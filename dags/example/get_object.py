from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.http.operators.http import HttpOperator

@dag(schedule_interval=None, start_date=days_ago(1), catchup=False)
def get_s3_object():
    @task
    def read_txt_file(ti=None):
            file_data = ti.xcom_pull(task_ids='get_txt_file')
            return file_data

    get_file = HttpOperator(
            task_id='get_txt_file',
            http_conn_id='spin_http',
            method='GET',
            headers={'x-uri-path': 'test1.txt'},
    )

    read_file_data = read_txt_file()

    get_file >> read_file_data

get_s3_object = get_s3_object()
