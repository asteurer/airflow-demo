from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.http.operators.http import HttpOperator

@dag(schedule_interval=None, start_date=days_ago(1), catchup=False)
def put_s3_object():
    @task
    def create_file():
        message = 'Hello there!'
        return message
    
    string_content = create_file()
    put_object = HttpOperator(
        task_id='put_confirmation_xml',
        http_conn_id='spin_http',
        method='PUT',
        headers={'x-uri-path': 'test1.txt'},
        data="{{ ti.xcom_pull(task_ids='create_file') }}"
    )

    string_content >> put_object

delete_s3_object = put_s3_object()

