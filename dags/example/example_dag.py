from datetime import datetime

from airflow.decorators import task
from airflow.models.dag import dag


@task
def task_one():
    return [1, 2, 3, 4]


@task
def task_two(numbers):
    return sum(numbers)


@dag(dag_id="example_dag",
     schedule=None,
     start_date=datetime(2020, 1, 1),
     )
def example_dag():
    task_two(numbers=task_one())


exported_dag = example_dag()
