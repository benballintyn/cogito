"""
Custom sentence tokenizer to split text into sentences while handling abbreviations and punctuation.
"""

import re

# Extended list of abbreviations
ABBREVIATIONS = {
    "Dr.",
    "Mr.",
    "Mrs.",
    "Ms.",
    "Prof.",
    "Sr.",
    "Jr.",
    "Rev.",
    "Fr.",
    "St.",
    "e.g.",
    "i.e.",
    "etc.",
    "et al.",
    "vs.",
    "viz.",
    "ca.",
    "U.S.",
    "U.K.",
    "E.U.",
    "A.M.",
    "P.M.",
    "in.",
    "ft.",
    "lb.",
    "oz.",
    "cm.",
    "mm.",
    "km.",
    "kg.",
    "mg.",
    "ml.",
    "hr.",
    "No.",
    "Inc.",
    "Co.",
    "Ltd.",
    "Corp.",
    "Fig.",
    "Eq.",
    "Ex.",
    "Ch.",
    "Vol.",
}

# Common continuation words
CONTINUATION_WORDS = {
    "and",
    "or",
    "but",
    "if",
    "then",
    "because",
    "while",
    "however",
    "although",
    "though",
}


def custom_sent_tokenize(text: str) -> list[str]:
    """
    Tokenize a string into sentences, handling abbreviations and punctuation.

    Args:
        text (str): The input text to tokenize.

    Returns:
        list[str]: A list of sentences.
    """
    if not text:
        return []

    # Escape abbreviations to prevent splitting on them
    for abbr in ABBREVIATIONS:
        text = text.replace(abbr, abbr.replace(".", "<DOT>"))

    # Split on sentence-ending punctuation, restoring abbreviations
    raw_sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", text.strip())

    # Restore abbreviations and filter out empty strings or whitespace
    sentences = [
        sentence.replace("<DOT>", ".").strip()
        for sentence in raw_sentences
        if sentence.strip()
    ]

    return sentences
