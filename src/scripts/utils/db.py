import logging
import os
import sys

import mysql.connector
import psycopg2

logger = logging.getLogger()
logger.setLevel(logging.INFO)

handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s::: %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


class Database:

    def __init__(self):
        self.mysql_conn = self.get_mysql_connection()
        self.postgresql_conn = self.get_postgresql_connection()

    def get_mysql_connection(self):
        dbname = os.environ['MYSQL_DATABASE']
        user = os.environ['MYSQL_user']
        password = os.environ['MYSQL_ROOT_PASSWORD']
        host = os.environ['MYSQL_HOST']
        port = int(os.environ['MYSQL_PORT'])
        conn = None
        try:
            conn = mysql.connector.connect(
                host=host, user=user, password=password.strip(), database=dbname, port=port)
        except Exception as e:
            logger.info(f"Unable to connect to mysql database.\nError: {e}")
        return conn

    def get_postgresql_connection(self):
        dbname = os.environ['POSTGRES_DB']
        user = os.environ['POSTGRES_USER']
        password = os.environ['POSTGRES_PASSWORD']
        host = os.environ['POSTGRES_HOST']
        port = int(os.environ['POSTGRES_PORT'])
        conn_string = f"dbname={dbname} user={user} password={password} host={host} port={port}"
        conn = None
        try:
            conn = psycopg2.connect(conn_string)
        except Exception as e:
            logger.info(
                f"Unable to connect to postgresql database.\nError: {e}")
        return conn


if __name__ == "__main__":
    pass
