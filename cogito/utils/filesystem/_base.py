import json
import pickle
from abc import ABC, abstractmethod
from typing import Any, List

import pandas as pd
import yaml


class FileSystem(ABC):
    """Abstract base class for file system operations."""

    @abstractmethod
    def list_files(self, path: str) -> List[str]:
        """
        List files in a directory.

        Args:
            path (str): Path to the directory.

        Returns:
            list[str]: List of file names in the directory.
        """
        pass

    @abstractmethod
    def copy_file(self, source: str, destination: str) -> None:
        """
        Copy a file from source to destination.

        Args:
            source (str): Path to the source file.
            destination (str): Path to the destination file.
        """
        pass

    @abstractmethod
    def upload_file(self, local_path: str, remote_path: str) -> None:
        """
        Upload a file from local storage to the remote file system.

        Args:
            local_path (str): Path to the local file.
            remote_path (str): Destination path in the remote file system.
        """
        pass

    @abstractmethod
    def download_file(self, remote_path: str, local_path: str) -> None:
        """
        Download a file from the remote file system to local storage.

        Args:
            remote_path (str): Path to the remote file.
            local_path (str): Destination path in the local file system.
        """
        pass

    @abstractmethod
    def delete_file(self, path: str) -> None:
        """
        Delete a file from the file system.

        Args:
            path (str): Path to the file to be deleted.
        """
        pass

    # Read Methods
    def read_json(self, path: str) -> Any:
        """
        Read a JSON file.

        Args:
            path (str): Path to the JSON file.

        Returns:
            Any: Parsed JSON data.
        """
        with open(path, "r") as f:
            return json.load(f)

    def read_yaml(self, path: str) -> Any:
        """
        Read a YAML file.

        Args:
            path (str): Path to the YAML file.

        Returns:
            Any: Parsed YAML data.
        """
        with open(path, "r") as f:
            return yaml.safe_load(f)

    def read_csv(self, path: str) -> pd.DataFrame:
        """
        Read a CSV file.

        Args:
            path (str): Path to the CSV file.

        Returns:
            pd.DataFrame: Data from the CSV file.
        """
        return pd.read_csv(path)

    def read_parquet(self, path: str) -> pd.DataFrame:
        """
        Read a Parquet file.

        Args:
            path (str): Path to the Parquet file.

        Returns:
            pd.DataFrame: Data from the Parquet file.
        """
        return pd.read_parquet(path)

    def read_text(self, path: str) -> str:
        """
        Read a text file.

        Args:
            path (str): Path to the text file.

        Returns:
            str: Content of the text file.
        """
        with open(path, "r") as f:
            return f.read()

    def read_pickle(self, path: str) -> Any:
        """
        Read a Pickle file.

        Args:
            path (str): Path to the Pickle file.

        Returns:
            Any: Deserialized Python object.
        """
        with open(path, "rb") as f:
            return pickle.load(f)

    # Write Methods
    def write_json(self, path: str, data: Any) -> None:
        """
        Write data to a JSON file.

        Args:
            path (str): Path to the JSON file.
            data (Any): Data to write.
        """
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def write_yaml(self, path: str, data: Any) -> None:
        """
        Write data to a YAML file.

        Args:
            path (str): Path to the YAML file.
            data (Any): Data to write.
        """
        with open(path, "w") as f:
            yaml.safe_dump(data, f)

    def write_csv(self, path: str, data: pd.DataFrame) -> None:
        """
        Write a DataFrame to a CSV file.

        Args:
            path (str): Path to the CSV file.
            data (pd.DataFrame): DataFrame to write.
        """
        data.to_csv(path, index=False)

    def write_parquet(self, path: str, data: pd.DataFrame) -> None:
        """
        Write a DataFrame to a Parquet file.

        Args:
            path (str): Path to the Parquet file.
            data (pd.DataFrame): DataFrame to write.
        """
        data.to_parquet(path, index=False)

    def write_text(self, path: str, data: str) -> None:
        """
        Write data to a text file.

        Args:
            path (str): Path to the text file.
            data (str): Text content.
        """
        with open(path, "w") as f:
            f.write(data)

    def write_pickle(self, path: str, data: Any) -> None:
        """
        Write data to a Pickle file.

        Args:
            path (str): Path to the Pickle file.
            data (Any): Python object to serialize.
        """
        with open(path, "wb") as f:
            pickle.dump(data, f)
