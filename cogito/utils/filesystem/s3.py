import io
import json
from typing import Any, List, Optional

import boto3
import pandas as pd
import yaml
from botocore.exceptions import BotoCoreError, ClientError
from loguru import logger

from ._base import FileSystem


class S3FileSystem(FileSystem):
    """Class to interact with AWS S3 using boto3."""

    def __init__(self, bucket_name: str, region: Optional[str] = None):
        """
        Initialize S3 client.

        Args:
            bucket_name (str): Name of the S3 bucket.
            region (Optional[str]): AWS region.

        Raises:
            BotoCoreError: If boto3 encounters an error.
        """
        self.bucket_name = bucket_name
        try:
            self.s3 = boto3.client("s3", region_name=region)
        except BotoCoreError as e:
            logger.error(f"Failed to initialize S3 client: {e}")
            raise

    def list_files(self, prefix: str = "") -> List[str]:
        """
        List files in an S3 bucket under a given prefix.

        Args:
            prefix (str, optional): Prefix to filter files. Defaults to "".

        Returns:
            list[str]: List of file paths.

        Raises:
            ClientError: If the S3 request fails.
        """
        try:
            response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=prefix)
            return [obj["Key"] for obj in response.get("Contents", [])]
        except ClientError as e:
            logger.error(f"Failed to list files in S3: {e}")
            raise

    def copy_file(self, source: str, destination: str) -> None:
        """
        Copy a file within S3.

        Args:
            source (str): Source file path in S3.
            destination (str): Destination file path in S3.

        Raises:
            ClientError: If the copy operation fails.
        """
        try:
            copy_source = {"Bucket": self.bucket_name, "Key": source}
            self.s3.copy(copy_source, self.bucket_name, destination)
        except ClientError as e:
            logger.error(f"Failed to copy file in S3: {e}")
            raise

    def upload_file(self, local_path: str, remote_path: str) -> None:
        """
        Upload a local file to S3.

        Args:
            local_path (str): Path to the local file.
            remote_path (str): Destination path in S3.

        Raises:
            ClientError: If the upload operation fails.
        """
        try:
            self.s3.upload_file(local_path, self.bucket_name, remote_path)
        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise

    def download_file(self, remote_path: str, local_path: str) -> None:
        """
        Download a file from S3 to local storage.

        Args:
            remote_path (str): Path to the file in S3.
            local_path (str): Destination path in local storage.

        Raises:
            ClientError: If the download operation fails.
        """
        try:
            self.s3.download_file(self.bucket_name, remote_path, local_path)
        except ClientError as e:
            logger.error(f"Failed to download file from S3: {e}")
            raise

    def delete_file(self, path: str) -> None:
        """
        Delete a file from S3.

        Args:
            path (str): Path to the file in S3.

        Raises:
            ClientError: If the delete operation fails.
        """
        try:
            self.s3.delete_object(Bucket=self.bucket_name, Key=path)
        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {e}")
            raise

    # Read and Write Methods
    def read_json(self, path: str) -> Any:
        """
        Read a JSON file from S3.

        Args:
            path (str): Path to the JSON file in S3.

        Returns:
            Any: Parsed JSON data.

        Raises:
            ClientError: If the file cannot be retrieved from S3.
            json.JSONDecodeError: If the file is not a valid JSON.
        """
        obj = self.s3.get_object(Bucket=self.bucket_name, Key=path)
        return json.load(io.BytesIO(obj["Body"].read()))

    def write_json(self, path: str, data: Any) -> None:
        """
        Write data to a JSON file in S3.

        Args:
            path (str): Path to the JSON file in S3.
            data (Any): Data to be written.

        Raises:
            ClientError: If the file cannot be uploaded to S3.
        """
        try:
            self.s3.put_object(Bucket=self.bucket_name, Key=path, Body=json.dumps(data))
        except ClientError as e:
            logger.error(f"Failed to write JSON file to S3: {e}")
            raise

    def read_yaml(self, path: str) -> Any:
        """
        Read a YAML file from S3.

        Args:
            path (str): Path to the YAML file in S3.

        Returns:
            Any: Parsed YAML data.

        Raises:
            ClientError: If the file cannot be retrieved from S3.
            yaml.YAMLError: If the file is not a valid YAML.
        """
        obj = self.s3.get_object(Bucket=self.bucket_name, Key=path)
        return yaml.safe_load(io.BytesIO(obj["Body"].read()))

    def write_yaml(self, path: str, data: Any) -> None:
        """
        Write data to a YAML file in S3.

        Args:
            path (str): Path to the YAML file in S3.
            data (Any): Data to be written.

        Raises:
            ClientError: If the file cannot be uploaded to S3.
        """
        try:
            self.s3.put_object(
                Bucket=self.bucket_name, Key=path, Body=yaml.safe_dump(data)
            )
        except ClientError as e:
            logger.error(f"Failed to write YAML file to S3: {e}")
            raise

    def read_csv(self, path: str) -> pd.DataFrame:
        """
        Read a CSV file from S3.

        Args:
            path (str): Path to the CSV file in S3.

        Returns:
            pd.DataFrame: Data from the CSV file.

        Raises:
            ClientError: If the file cannot be retrieved from S3.
            pd.errors.ParserError: If the file cannot be parsed as CSV.
        """
        obj = self.s3.get_object(Bucket=self.bucket_name, Key=path)
        return pd.read_csv(io.BytesIO(obj["Body"].read()))

    def write_csv(self, path: str, data: pd.DataFrame) -> None:
        """
        Write a DataFrame to a CSV file in S3.

        Args:
            path (str): Path to the CSV file in S3.
            data (pd.DataFrame): DataFrame to write.

        Raises:
            ClientError: If the file cannot be uploaded to S3.
        """
        csv_buffer = io.StringIO()
        data.to_csv(csv_buffer, index=False)
        try:
            self.s3.put_object(
                Bucket=self.bucket_name, Key=path, Body=csv_buffer.getvalue()
            )
        except ClientError as e:
            logger.error(f"Failed to write CSV file to S3: {e}")
            raise

    def read_parquet(self, path: str) -> pd.DataFrame:
        """
        Read a Parquet file from S3.

        Args:
            path (str): Path to the Parquet file in S3.

        Returns:
            pd.DataFrame: Data from the Parquet file.

        Raises:
            ClientError: If the file cannot be retrieved from S3.
        """
        obj = self.s3.get_object(Bucket=self.bucket_name, Key=path)
        return pd.read_parquet(io.BytesIO(obj["Body"].read()))

    def write_parquet(self, path: str, data: pd.DataFrame) -> None:
        """
        Write a DataFrame to a Parquet file in S3.

        Args:
            path (str): Path to the Parquet file in S3.
            data (pd.DataFrame): DataFrame to write.

        Raises:
            ClientError: If the file cannot be uploaded to S3.
        """
        parquet_buffer = io.BytesIO()
        data.to_parquet(parquet_buffer, index=False)
        try:
            self.s3.put_object(
                Bucket=self.bucket_name, Key=path, Body=parquet_buffer.getvalue()
            )
        except ClientError as e:
            logger.error(f"Failed to write Parquet file to S3: {e}")
            raise
