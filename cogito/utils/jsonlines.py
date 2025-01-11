"""
Utilities and classes for working with jsonlines files.
"""
from dataclasses import dataclass
from pathlib import Path
from typing import Generator

import jsonlines


def read_jsonlines(file_path: Path | str) -> Generator[dict, None, None]:
    """
    Read a jsonlines file line by line and yield the contents of each line.

    Args:
        file_path (Path | str): The path to the jsonlines file.

    Yields:
        dict: The contents of each line in the jsonlines file.
    """
    try:
        with jsonlines.open(file_path, "r") as reader:
            for line in reader:
                yield line
    except FileNotFoundError as exc:
        raise FileNotFoundError(f"File not found: {file_path}") from exc
    except jsonlines.Error as exc:
        raise jsonlines.Error(f"Error reading file: {file_path}") from exc


def write_jsonlines(file_path: Path | str, data: list[dict]) -> None:
    """
    Write a list of dictionaries to a new jsonlines file.

    Args:
        file_path (Path | str): The path to the jsonlines file.
        data (list[dict]): The list of dictionaries to write to the file.
    """
    with jsonlines.open(file_path, "w") as writer:
        writer.write_all(data)


def append_jsonlines(file_path: Path | str, data: list[dict]) -> None:
    """
    Append a list of dictionaries to an existing jsonlines file.

    Args:
        file_path (Path | str): The path to the jsonlines file.
        data (list[dict]): The list of dictionaries to append to the file.
    """
    with jsonlines.open(file_path, "a") as writer:
        writer.write_all(data)


@dataclass
class JsonlinesFile:
    """
    A class for working with jsonlines files.

    Attributes:
        file_path (Path): The path to the jsonlines file.
    """

    file_path: Path

    def read(self):
        """
        Read a jsonlines file line by line and yield the contents of each line.

        Yields:
            dict: The contents of each line in the jsonlines file.
        """
        read_jsonlines(self.file_path)

    def write(self, data: list[dict]) -> None:
        """
        Write a list of dictionaries to a new jsonlines file.

        Args:
            data (list[dict]): The list of dictionaries to write to the file.
        """
        with jsonlines.open(self.file_path, "w") as writer:
            writer.write_all(data)

    def append(self, data: list[dict]) -> None:
        """
        Append a list of dictionaries to an existing jsonlines file.

        Args:
            data (list[dict]): The list of dictionaries to append to the file.
        """
        with jsonlines.open(self.file_path, "a") as writer:
            writer.write_all(data)
