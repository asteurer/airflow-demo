import boto3
import logging
import os
from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.sftp.operators.sftp import SFTPOperator
from example.config import INPUT_FILE_NAME

session = boto3.Session(aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"), 
                        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"), 
                        aws_session_token=os.environ.get("AWS_SESSION_TOKEN"))

s3 = session.client('s3')

@dag(schedule_interval=None, start_date=days_ago(1), catchup=False)
def airflow_s3():
    get_file = SFTPOperator(
        task_id='get_file',
        ssh_conn_id='ftp_server',
        remote_filepath=INPUT_FILE_NAME,
        local_filepath=f'/tmp/{INPUT_FILE_NAME}',
        create_intermediate_dirs=True,
        operation='get'
    )

    @task
    def send_to_s3():
        try:            
            with open(f'/tmp/{INPUT_FILE_NAME}', 'rb') as file:
                s3.upload_fileobj(file, 'asteurer-cardoai-demo', INPUT_FILE_NAME)
        except Exception as e:
            logging.error(e)

    send_s3 = send_to_s3()

    get_file >> send_s3

airflow_s3 = airflow_s3()
