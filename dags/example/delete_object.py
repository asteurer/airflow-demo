from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.http.operators.http import HttpOperator

@dag(schedule_interval=None, start_date=days_ago(1), catchup=False)
def delete_s3_object():
    delete_object = HttpOperator(
        task_id='delete_confirmation_xml',
        http_conn_id='spin_http',
        method='DELETE',
        headers={'x-uri-path': 'test1.txt'},
    )

    delete_object

delete_s3_object = delete_s3_object()

