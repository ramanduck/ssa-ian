import subprocess
import boto3
import pandas as pd
import os
from io import StringIO
from datetime import datetime
import typer
from src.scripts.utils.db import Database, logger
import warnings

warnings.filterwarnings('ignore')
app = typer.Typer()


def run_cmd(cmd: str):
    proc = subprocess.Popen(cmd, shell=True)
    proc.communicate()


def get_report():
    try:
        database = Database()
        final_result = []
        chunk_size = 1000
        join_key = 'user_id'
        users_query = """SELECT user_id, user_name
                        FROM mindtickle_users
                        where active_status='active'"""
        for chunk in pd.read_sql_query(users_query, con=database.postgresql_conn, chunksize=chunk_size):
            join_keys = [int(key) for key in chunk[join_key].unique().tolist()]
            join_key_params = ', '.join(['%s'] * len(join_keys))
            lessons_query = f"""SELECT user_id, lesson_id
                                FROM lesson_completion
                                WHERE {join_key} IN ({join_key_params})
                                AND completion_date >= CURDATE() - INTERVAL 1 YEAR"""
            lesson_completion_data = pd.read_sql_query(lessons_query, con=database.mysql_conn, params=tuple(join_keys))
            joined_data = pd.merge(chunk, lesson_completion_data, on=join_key)
            result = joined_data.groupby(['user_id', 'user_name'])['lesson_id'].count()
            final_result.append(result.reset_index())
        final_result = pd.concat(final_result, axis=0).groupby(['user_id', 'user_name'])['lesson_id'].sum()
        final_result = final_result.reset_index().rename(columns={'lesson_id': 'lessons_completed'})
        return final_result
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return None
    finally:
        if database.postgresql_conn:
            database.postgresql_conn.close()
        if database.mysql_conn:
            database.mysql_conn.close()



def upload_report_to_s3(report, bucket_name):
    try:
        account_id = os.environ.get('AWS_ACCOUNT_ID')
        if not account_id:
            raise ValueError("AWS_ACCOUNT_ID is not found.")

        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        s3_key = f"{account_id}_data_{timestamp}.csv"
        csv_buffer = StringIO()
        report.to_csv(csv_buffer, index=False)

        s3_resource = boto3.resource('s3')
        s3_object = s3_resource.Object(bucket_name, s3_key)
        s3_object.put(Body=csv_buffer.getvalue())
        
        return f"https://{bucket_name}.s3.amazonaws.com/{s3_key}"
    except Exception as e:
        logger.info(f"An error occurred: {e}")
        return None


def lambda_handler(event, context):
    try:
        report = get_report()
        if report is not None and not report.empty:
            bucket_name = os.getenv('S3_BUCKET_NAME', 'mindtickle-daily-report').strip()
            upload_path = upload_report_to_s3(report, bucket_name)
            return {
                'statusCode': 200,
                'body': f"Report successfully uploaded to {upload_path}"
            }
        else:
            return {
                'statusCode': 500,
                'body': "Failed to generate report or report was empty"
            }
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return {
            'statusCode': 500,
            'body': str(e)
        }


@app.command()
def generate_report():
    report = get_report()
    logger.info(report)


@app.command()
def upload_report():
    report = get_report()
    path = upload_report_to_s3(report, bucket_name=os.getenv('S3_BUCKET_NAME', 'mindtickle-daily-report').strip())
    if path:
        logger.info(f"Successfully uploaded report to {path}")
    else:
        logger.info("Unable to upload report")


@app.command()
def unit_test():
    run_cmd(
        "pytest --cov=src src tests"
    )


def main():
    app()


if __name__ == "__main__":
    main()
