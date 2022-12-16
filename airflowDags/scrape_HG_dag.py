from api.main import main_func

from airflow.operators.python_operator import PythonOperator
from airflow import DAG
from datetime import datetime, timedelta



default_args={
        "depends_on_past": False,
        # "email": ["airflow@example.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=5),
        # 'queue': 'bash_queue',
        # 'pool': 'backfill',
        # 'priority_weight': 10,
        # 'end_date': datetime(2016, 1, 1),
        # 'wait_for_downstream': False,
        # 'sla': timedelta(hours=2),
        # 'execution_timeout': timedelta(seconds=300),
        # 'on_failure_callback': some_function,
        # 'on_success_callback': some_other_function,
        # 'on_retry_callback': another_function,
        # 'sla_miss_callback': yet_another_function,
        # 'trigger_rule': 'all_success'
    }


with DAG( "ScrapeHGDag", 
    default_args=default_args,
    description="A simple DAG that scrapes Homegate Website for specific zip codes", 
    schedule='*/30 * * * *', 
    start_date=datetime(2021, 1, 1),
    catchup=False,
    tags=["HomeGate", "RealEstateMarketAnalyzer"],
) as dag:


    # Instantiate the PythonOperator
    python_task = PythonOperator(
        task_id="SrapeHG",
        python_callable=main_func,
        op_kwargs={'zipcodes': [ '8002', '8005', '8000'], 'usage_type': 'rent'},
    )

python_task