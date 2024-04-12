import pytest
from unittest.mock import patch, MagicMock
from src.scripts.main import get_report, upload_report_to_s3, lambda_handler
import pandas as pd
import warnings

warnings.filterwarnings('ignore')


@pytest.fixture
def mock_database():
    with patch('src.scripts.utils.db.Database') as MockDatabase:
        db_instance = MockDatabase.return_value
        db_instance.postgresql_conn = MagicMock()
        db_instance.mysql_conn = MagicMock()
        yield db_instance


@pytest.fixture
def mock_s3_resource():
    with patch('boto3.resource') as mock:
        yield mock


@pytest.fixture
def mock_environment():
    with patch('os.getenv') as mock_env:
        mock_env.return_value = 'mindtickle-daily-report'
        yield mock_env


def test_lambda_handler_success(mock_environment):
    with patch('src.scripts.main.get_report') as mock_get_report, patch('src.scripts.main.upload_report_to_s3') as mock_upload_report:
        mock_report = MagicMock()
        mock_report.empty = False
        mock_get_report.return_value = mock_report
        mock_upload_report.return_value = "https://s3.amazonaws.com/mindtickle-daily-report/report.csv"

        response = lambda_handler({}, {})

        assert response['statusCode'] == 200
        assert "Report successfully uploaded to https://s3.amazonaws.com/mindtickle-daily-report/report.csv" in response['body']


def test_lambda_handler_empty_report(mock_environment):
    with patch('src.scripts.main.get_report') as mock_get_report:
        mock_report = MagicMock()
        mock_report.empty = True
        mock_get_report.return_value = mock_report

        response = lambda_handler({}, {})

        assert response['statusCode'] == 500
        assert "Failed to generate report or report was empty" in response['body']


def test_lambda_handler_exception(mock_environment):
    with patch('src.scripts.main.get_report', side_effect=Exception("Test Exception")) as mock_get_report:
        response = lambda_handler({}, {})

        assert response['statusCode'] == 500
        assert "Test Exception" in response['body']


@pytest.mark.filterwarnings("ignore:pandas only supports SQLAlchemy connectable")
def test_get_report_success(mock_database):
    mock_database.postgresql_conn.execute.return_value = iter([
        pd.DataFrame({'user_id': [1, 2], 'user_name': ['Alice', 'Bob']}),
        pd.DataFrame()
    ])
    mock_database.mysql_conn.execute.return_value = iter([
        pd.DataFrame({'user_id': [1], 'lesson_id': [101]}),
        pd.DataFrame()
    ])
    
    result = get_report()
    
    assert not result.empty
    assert 'lessons_completed' in result.columns


def test_upload_report_to_s3_success(mock_s3_resource):
    report = pd.DataFrame({'user_id': [1], 'lessons_completed': [10]})
    
    mock_s3 = mock_s3_resource.return_value
    mock_s3.Object.return_value.put.return_value = None
    
    with patch.dict('os.environ', {'AWS_ACCOUNT_ID': '123456789012'}):
        result = upload_report_to_s3(report, "test-bucket")
    
    assert "https://test-bucket.s3.amazonaws.com/" in result


def test_upload_report_to_s3_failure(mock_s3_resource):
    report = pd.DataFrame({'user_id': [1], 'lessons_completed': [10]})
    
    mock_s3 = mock_s3_resource.return_value
    mock_s3.Object.return_value.put.side_effect = Exception("Upload failed")
    
    with patch.dict('os.environ', {'AWS_ACCOUNT_ID': '123456789012'}):
        result = upload_report_to_s3(report, "test-bucket")
    
    assert result is None
