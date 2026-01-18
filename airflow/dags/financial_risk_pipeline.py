from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'mlops',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'financial_risk_retraining',
    default_args=default_args,
    description='End-to-end retraining pipeline',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
) as dag:

    # 1. Generate Data (For simulation)
    generate_data = BashOperator(
        task_id='generate_data',
        bash_command='python /opt/mlops/features/generate_data.py'
    )

    # 2. Materialize Feature Store (Offline -> Online)
    # Assumes 'feast' is installed and configured in the environment
    # Using 'feast materialize' to sync latest data to Redis
    # In a real setup, this path would be mapped or git-synced
    materialize_features = BashOperator(
        task_id='materialize_features',
        bash_command='cd /opt/mlops/features && feast materialize-incremental $(date +%Y-%m-%d)'
    )

    # 3. Train Model
    train_model = BashOperator(
        task_id='train_model',
        bash_command='python /opt/mlops/training/train.py --feature_repo /opt/mlops/features'
    )

    generate_data >> materialize_features >> train_model

