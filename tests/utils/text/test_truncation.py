import pytest
import tiktoken

from cogito.utils.text.truncation import truncate


# Custom tokenizer (splits by spaces)
def custom_tokenizer(text: str) -> list[str]:
    return text.split()


def test_truncate_with_tiktoken():
    text = "This is a test sentence to demonstrate truncation functionality."
    encoding = tiktoken.encoding_for_model("gpt-4")
    truncated = truncate(text, max_tokens=10, model="gpt-4")
    tokens = encoding.encode(truncated)

    assert len(tokens) <= 10
    assert "truncation" in truncated


def test_truncate_with_custom_tokenizer():
    # Example input and token limit
    text = "This is a test sentence to demonstrate truncation functionality."

    # Truncate using custom tokenizer
    truncated = truncate(text, max_tokens=5, tokenizer=custom_tokenizer)

    # Ensure the truncated text has 5 tokens
    assert truncated == "This is a test sentence"


def test_truncate_from_start_with_tiktoken():
    # Example input and token limit
    text = "This is a test sentence to demonstrate truncation functionality."

    # Truncate from the start using tiktoken
    truncated = truncate(text, max_tokens=10, model="gpt-4", truncate_from="start")

    # Check the result
    tokens = tiktoken.encoding_for_model("gpt-4").encode(text)
    expected_tokens = tokens[-10:]  # Tokens kept from the start
    expected_text = tiktoken.encoding_for_model("gpt-4").decode(expected_tokens)

    assert truncated == expected_text


def test_truncate_with_empty_text():
    # Empty input
    text = ""

    # Truncate using tiktoken
    truncated = truncate(text, max_tokens=10, model="gpt-4")

    # Ensure the output is still empty
    assert truncated == ""


def test_truncate_with_invalid_max_tokens():
    # Example input
    text = "This is a test sentence."

    # Test with invalid max_tokens
    with pytest.raises(ValueError, match="max_tokens must be a positive integer."):
        truncate(text, max_tokens=0)

    with pytest.raises(ValueError, match="max_tokens must be a positive integer."):
        truncate(text, max_tokens=-5)


def test_truncate_with_invalid_truncate_from():
    # Example input
    text = "This is a test sentence."

    # Test with invalid truncate_from
    with pytest.raises(ValueError, match="truncate_from must be 'end' or 'start'."):
        truncate(text, max_tokens=5, truncate_from="middle")
