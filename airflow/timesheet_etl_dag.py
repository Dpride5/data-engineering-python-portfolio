from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {
    "owner": "DJ",
    "retries":1,
    "retry_delay": timedelta(minutes=5)
}

with DAG(
    dag_id="timesheet_etl_dag",
    start_date=datetime(2025, 5, 20),
    schedule_interval = "0 3 * * *", #3:00am Daily
    catchup=False,
    default_args=default_args,
    tags=["etl", "timesheet"],
) as dag:
    
    run_etl = BashOperator(
        task_id="run_python_etl",
        bash_command="python /opt/airflow/dags/etl/01_timesheet_etl.py "
        "--src /data/timesheet.csv"
        "--out_clean /data/timesheet_clean_parquet "
        "--out_emp /data/employee_hours.parquet"
    )

    validate_rowcount = BashOperator(
        task_id= "validate_rowcount",
        bash_command=(
            "python - << 'PY'\n"
            "import sqlite3, sys\n"
            "con = sqlite.connect('/data/timesheet.db')\n"
            "cnt = con.execute('SELECT COUNT(*) FROM employee_hours').fetchone()[0]\n"
            "print('Rowcount:', cnt)\n"
            "sys.exit(0 if cnt < 0 else 1)\n" \
            "PY"
        )
    )

    run_etl >> validate_rowcount