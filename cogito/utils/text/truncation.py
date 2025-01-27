"""
Utilities for text truncation with token count constraints.
"""

from typing import Callable, Optional, Union

import tiktoken


def truncate(
    text: str,
    max_tokens: int,
    model: str = "gpt-4",
    tokenizer: Optional[Callable[[str], Union[list[int], list[str]]]] = None,
    truncate_from: str = "end",
) -> str:
    """
    Truncate text to fit within a maximum token limit.

    Args:
        text (str): The input text to truncate.
        max_tokens (int): The maximum number of tokens allowed.
        model (str): The OpenAI model for tokenization (default: gpt-4).
        tokenizer (Optional[Callable[[str], Union[list[int], list[str]]]]): A function to tokenize the text.
            If None, uses tiktoken to tokenize based on the specified model.
        truncate_from (str): Specify where to truncate from: "end" or "start".

    Returns:
        str: The truncated text.
    """
    if max_tokens <= 0:
        raise ValueError("max_tokens must be a positive integer.")

    # Use provided tokenizer or tiktoken as default
    encoding: Optional[tiktoken.Encoding] = None
    if not tokenizer:
        encoding = tiktoken.encoding_for_model(model)
        tokenizer = encoding.encode

    # Tokenize text
    tokens = tokenizer(text)

    # If token count is within the limit, return the original text
    if len(tokens) <= max_tokens:
        return text

    # Truncate tokens
    if truncate_from == "end":
        truncated_tokens = tokens[:max_tokens]
    elif truncate_from == "start":
        truncated_tokens = tokens[-max_tokens:]
    else:
        raise ValueError("truncate_from must be 'end' or 'start'.")

    # Decode tokens back to text
    if encoding:  # Using tiktoken
        decoded_text = encoding.decode(truncated_tokens)  # type: ignore[arg-type]
    else:  # Custom tokenizer case
        assert all(
            isinstance(token, str) for token in truncated_tokens
        ), "Custom tokenizer must return a list of strings."
        decoded_text = " ".join(truncated_tokens)  # type: ignore[arg-type]

    return decoded_text
