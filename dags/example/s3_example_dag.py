import boto3
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from deltalake import DeltaTable, Schema, Field
from deltalake.exceptions import TableNotFoundError
from deltalake.writer import write_deltalake

from example.config import (bucket_name, s3_endpoint_url, delta_location, INPUT_FILE_NAME, state_table_name,
                            database_name)
from example.utils import read_from_sftp

s3_client = boto3.client('s3', endpoint_url=s3_endpoint_url)
s3_client.create_bucket(Bucket=bucket_name)


@dag(schedule_interval=None, start_date=days_ago(1), catchup=False)
def s3_example_dag():
    @task
    def create_if_not_exist_table():
        print(f" Checking if the table {database_name}.{state_table_name} exists. If not, lets create it")
        table_uri = f"{bucket_name}/{delta_location}/{state_table_name}"
        try:
            dt = DeltaTable(table_uri=table_uri)
            print(" ------------------------ ", dt.schema())
        except TableNotFoundError:
            print("Table not found, creating it")
            schema = Schema([Field("state", "string"), Field("total_sales", "double")])
            dt = DeltaTable.create(table_uri=table_uri, schema=schema)
            print(f"Created table with schema {dt.schema()}")

    @task
    def read_input_from_sftp(db_exists):
        sftp_file_path = f"/sample_files/{INPUT_FILE_NAME}"
        input_data = read_from_sftp(sftp_file_path=sftp_file_path)
        print(f"Downloaded file content")

        return input_data

    @task
    def aggregate_and_write_to_delta(raw_data):
        table_uri = f"{bucket_name}/{delta_location}/{state_table_name}"

        state_df = raw_data.groupby(['State or Province'], as_index=False).agg({'Sales': 'sum'})
        state_df = state_df.rename(columns={'Sales': 'total_sales', 'State or Province': 'state'})
        write_deltalake(table_or_uri=table_uri, data=state_df, mode="overwrite", overwrite_schema=True)

    db_exists = create_if_not_exist_table()
    raw_data = read_input_from_sftp(db_exists)
    aggregate_and_write_to_delta(raw_data)


s3_example_dag = s3_example_dag()
