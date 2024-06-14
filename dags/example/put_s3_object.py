from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.http.operators.http import HttpOperator
from airflow.providers.sftp.operators.sftp import SFTPOperator

@dag(schedule_interval=None, start_date=days_ago(1), catchup=False)
def put_s3_object():
    get_file = SFTPOperator(
        task_id='get_file',
        ssh_conn_id='ftp_server',
        remote_filepath='file.txt',
        local_filepath='/tmp/file.txt',
        create_intermediate_dirs=True,
        operation='get'
    )

    @task
    def read_file():
        with open('/tmp/file.txt', 'rb') as file:
            return file.read().decode('utf-8')

    file_content = read_file()

    send_to_s3 = HttpOperator(
        task_id='place_in_s3',
        http_conn_id='spin_http',
        method='PUT',
        headers={'x-uri-path': 'file.txt'},
        data="{{ ti.xcom_pull(task_ids='read_file') }}"
    )

    get_file >> file_content >> send_to_s3

put_s3_object = put_s3_object()
