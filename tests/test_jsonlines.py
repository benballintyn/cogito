"""
Tests for the jsonlines utils module.
"""
import jsonlines
import pytest

from cogito.utils.jsonlines import (
    JsonlinesFile,
    append_jsonlines,
    read_jsonlines,
    write_jsonlines,
)


@pytest.fixture
def temp_jsonl_file(tmp_path):
    return tmp_path / "test.jsonl"


def test_read_jsonlines(temp_jsonl_file):
    data = [{"key1": "value1"}, {"key2": "value2"}]
    with jsonlines.open(temp_jsonl_file, "w") as writer:
        writer.write_all(data)

    result = list(read_jsonlines(temp_jsonl_file))
    assert result == data


def test_write_jsonlines(temp_jsonl_file):
    data = [{"key1": "value1"}, {"key2": "value2"}]
    write_jsonlines(temp_jsonl_file, data)

    with jsonlines.open(temp_jsonl_file, "r") as reader:
        result = list(reader)
    assert result == data


def test_append_jsonlines(temp_jsonl_file):
    initial_data = [{"key1": "value1"}]
    append_data = [{"key2": "value2"}]
    with jsonlines.open(temp_jsonl_file, "w") as writer:
        writer.write_all(initial_data)

    append_jsonlines(temp_jsonl_file, append_data)

    with jsonlines.open(temp_jsonl_file, "r") as reader:
        result = list(reader)
    assert result == initial_data + append_data


def test_jsonlinesfile_read(temp_jsonl_file):
    data = [{"key1": "value1"}, {"key2": "value2"}]
    with jsonlines.open(temp_jsonl_file, "w") as writer:
        writer.write_all(data)

    jsonlines_file = JsonlinesFile(file_path=temp_jsonl_file)
    result = list(jsonlines_file.read())
    assert result == data


def test_jsonlinesfile_write(temp_jsonl_file):
    data = [{"key1": "value1"}, {"key2": "value2"}]
    jsonlines_file = JsonlinesFile(file_path=temp_jsonl_file)
    jsonlines_file.write(data)

    with jsonlines.open(temp_jsonl_file, "r") as reader:
        result = list(reader)
    assert result == data


def test_jsonlinesfile_append(temp_jsonl_file):
    initial_data = [{"key1": "value1"}]
    append_data = [{"key2": "value2"}]
    with jsonlines.open(temp_jsonl_file, "w") as writer:
        writer.write_all(initial_data)

    jsonlines_file = JsonlinesFile(file_path=temp_jsonl_file)
    jsonlines_file.append(append_data)

    with jsonlines.open(temp_jsonl_file, "r") as reader:
        result = list(reader)
    assert result == initial_data + append_data
