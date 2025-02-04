import io
import json

import pandas as pd
import pytest
import yaml

from cogito.utils.filesystem.s3 import S3FileSystem


@pytest.fixture
def mock_s3(mocker):
    """Mock the S3 client."""
    mock_s3_client = mocker.Mock()
    mocker.patch("boto3.client", return_value=mock_s3_client)
    return mock_s3_client


@pytest.fixture
def s3_fs():
    """Initialize S3FileSystem with a mock bucket."""
    return S3FileSystem(bucket_name="mock-bucket")


def test_list_files(mock_s3, s3_fs):
    """Test listing files in S3."""
    mock_s3.list_objects_v2.return_value = {
        "Contents": [{"Key": "file1.txt"}, {"Key": "file2.txt"}]
    }

    files = s3_fs.list_files()
    assert files == ["file1.txt", "file2.txt"]
    mock_s3.list_objects_v2.assert_called_once_with(Bucket="mock-bucket", Prefix="")


def test_upload_file(mock_s3, s3_fs):
    """Test uploading a file to S3."""
    s3_fs.upload_file("local.txt", "remote.txt")
    mock_s3.upload_file.assert_called_once_with(
        "local.txt", "mock-bucket", "remote.txt"
    )


def test_download_file(mock_s3, s3_fs):
    """Test downloading a file from S3."""
    s3_fs.download_file("remote.txt", "local.txt")
    mock_s3.download_file.assert_called_once_with(
        "mock-bucket", "remote.txt", "local.txt"
    )


def test_delete_file(mock_s3, s3_fs):
    """Test deleting a file from S3."""
    s3_fs.delete_file("remote.txt")
    mock_s3.delete_object.assert_called_once_with(
        Bucket="mock-bucket", Key="remote.txt"
    )


def test_copy_file(mock_s3, s3_fs):
    """Test copying a file within S3."""
    s3_fs.copy_file("source.txt", "destination.txt")
    mock_s3.copy.assert_called_once_with(
        {"Bucket": "mock-bucket", "Key": "source.txt"},
        "mock-bucket",
        "destination.txt",
    )


def test_read_json(mock_s3, s3_fs):
    """Test reading a JSON file from S3."""
    json_data = {"key": "value"}
    mock_s3.get_object.return_value = {
        "Body": io.BytesIO(json.dumps(json_data).encode())
    }

    result = s3_fs.read_json("file.json")
    assert result == json_data
    mock_s3.get_object.assert_called_once_with(Bucket="mock-bucket", Key="file.json")


def test_write_json(mock_s3, s3_fs):
    """Test writing a JSON file to S3."""
    data = {"key": "value"}
    s3_fs.write_json("file.json", data)

    mock_s3.put_object.assert_called_once()
    args, kwargs = mock_s3.put_object.call_args
    assert kwargs["Bucket"] == "mock-bucket"
    assert kwargs["Key"] == "file.json"
    assert json.loads(kwargs["Body"]) == data


def test_read_yaml(mock_s3, s3_fs):
    """Test reading a YAML file from S3."""
    yaml_data = {"key": "value"}
    mock_s3.get_object.return_value = {
        "Body": io.BytesIO(yaml.safe_dump(yaml_data).encode())
    }

    result = s3_fs.read_yaml("file.yaml")
    assert result == yaml_data
    mock_s3.get_object.assert_called_once_with(Bucket="mock-bucket", Key="file.yaml")


def test_write_yaml(mock_s3, s3_fs):
    """Test writing a YAML file to S3."""
    data = {"key": "value"}
    s3_fs.write_yaml("file.yaml", data)

    mock_s3.put_object.assert_called_once()
    args, kwargs = mock_s3.put_object.call_args
    assert kwargs["Bucket"] == "mock-bucket"
    assert kwargs["Key"] == "file.yaml"
    assert yaml.safe_load(kwargs["Body"]) == data


def test_read_csv(mock_s3, s3_fs):
    """Test reading a CSV file from S3."""
    csv_data = "col1,col2\n1,2\n3,4"
    mock_s3.get_object.return_value = {"Body": io.BytesIO(csv_data.encode())}

    result = s3_fs.read_csv("file.csv")
    expected_df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    pd.testing.assert_frame_equal(result, expected_df)
    mock_s3.get_object.assert_called_once_with(Bucket="mock-bucket", Key="file.csv")


def test_write_csv(mock_s3, s3_fs):
    """Test writing a CSV file to S3."""
    df = pd.DataFrame({"col1": [1, 3], "col2": [2, 4]})
    s3_fs.write_csv("file.csv", df)

    mock_s3.put_object.assert_called_once()
    args, kwargs = mock_s3.put_object.call_args
    assert kwargs["Bucket"] == "mock-bucket"
    assert kwargs["Key"] == "file.csv"


def test_read_parquet(mock_s3, s3_fs):
    """Test reading a Parquet file from S3."""
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer)
    mock_s3.get_object.return_value = {"Body": io.BytesIO(parquet_buffer.getvalue())}

    result = s3_fs.read_parquet("file.parquet")
    pd.testing.assert_frame_equal(result, df)
    mock_s3.get_object.assert_called_once_with(Bucket="mock-bucket", Key="file.parquet")


def test_write_parquet(mock_s3, s3_fs):
    """Test writing a Parquet file to S3."""
    df = pd.DataFrame({"col1": [1, 2], "col2": [3, 4]})
    s3_fs.write_parquet("file.parquet", df)

    mock_s3.put_object.assert_called_once()
    args, kwargs = mock_s3.put_object.call_args
    assert kwargs["Bucket"] == "mock-bucket"
    assert kwargs["Key"] == "file.parquet"


def test_read_text(mock_s3, s3_fs):
    """Test reading a text file from S3."""
    text_data = "Hello, world!"
    mock_s3.get_object.return_value = {"Body": io.BytesIO(text_data.encode())}

    result = s3_fs.read_text("file.txt")
    assert result == text_data
    mock_s3.get_object.assert_called_once_with(Bucket="mock-bucket", Key="file.txt")


def test_write_text(mock_s3, s3_fs):
    """Test writing a text file to S3."""
    text_data = "Hello, world!"
    s3_fs.write_text("file.txt", text_data)

    mock_s3.put_object.assert_called_once()
    args, kwargs = mock_s3.put_object.call_args
    assert kwargs["Bucket"] == "mock-bucket"
    assert kwargs["Key"] == "file.txt"
    assert kwargs["Body"].decode("utf-8") == text_data
