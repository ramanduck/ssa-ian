import pytest
from unittest.mock import patch
from src.scripts.utils.db import Database

def test_get_mysql_connection_success(mocker):
    mocker.patch.dict('os.environ', {
        'MYSQL_DATABASE': 'test_db',
        'MYSQL_user': 'user',
        'MYSQL_ROOT_PASSWORD': 'pass',
        'MYSQL_HOST': 'localhost',
        'MYSQL_PORT': '3306'
    })
    
    mocker.patch('mysql.connector.connect', return_value="mock_mysql_connection")

    db = Database()
    result = db.get_mysql_connection()

    assert result == "mock_mysql_connection", "Should return a mock connection object"

def test_get_mysql_connection_failure(mocker):
    mocker.patch.dict('os.environ', {
        'MYSQL_DATABASE': 'test_db',
        'MYSQL_user': 'user',
        'MYSQL_ROOT_PASSWORD': 'pass',
        'MYSQL_HOST': 'localhost',
        'MYSQL_PORT': '3306'
    })
    
    mocker.patch('mysql.connector.connect', side_effect=Exception("Connection failed"))

    db = Database()
    result = db.get_mysql_connection()

    assert result is None, "Should return None on failure"

def test_get_postgresql_connection_success(mocker):
    mocker.patch.dict('os.environ', {
        'POSTGRES_DB': 'test_db',
        'POSTGRES_USER': 'user',
        'POSTGRES_PASSWORD': 'pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432'
    })
    
    mocker.patch('psycopg2.connect', return_value="mock_postgresql_connection")

    db = Database()
    result = db.get_postgresql_connection()

    assert result == "mock_postgresql_connection", "Should return a mock connection object"

def test_get_postgresql_connection_failure(mocker):
    mocker.patch.dict('os.environ', {
        'POSTGRES_DB': 'test_db',
        'POSTGRES_USER': 'user',
        'POSTGRES_PASSWORD': 'pass',
        'POSTGRES_HOST': 'localhost',
        'POSTGRES_PORT': '5432'
    })
    
    mocker.patch('psycopg2.connect', side_effect=Exception("Connection failed"))

    db = Database()
    result = db.get_postgresql_connection()

    assert result is None, "Should return None on failure"
