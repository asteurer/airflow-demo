from airflow.decorators import dag, task
from airflow.utils.dates import days_ago
from airflow.providers.http.operators.http import HttpOperator
import xmltodict
import json

@dag(schedule_interval=None, start_date=days_ago(1), catchup=False)
def list_s3_objects():
    @task
    def parse_xml_to_json(ti=None):
        xml_data = ti.xcom_pull(task_ids='s3_objects_xml')
        xml_dict = xmltodict.parse(xml_data)
        json_string = json.dumps(xml_dict, indent=4)
        return json_string
    
    get_s3_xml = HttpOperator(
        task_id='s3_objects_xml',
        http_conn_id='spin_http',
        method='GET',
        headers={},
    )

    parsed_json = parse_xml_to_json()

    get_s3_xml >> parsed_json

list_s3_objects = list_s3_objects()

