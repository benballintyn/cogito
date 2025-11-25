import pytest

from cogito.utils.text.tokenizers import custom_sent_tokenize


@pytest.mark.parametrize(
    "text, expected",
    [
        # Basic sentences
        (
            "This is a sentence. And another one!",
            ["This is a sentence.", "And another one!"],
        ),
        ("Is this working? Yes, it is.", ["Is this working?", "Yes, it is."]),
        # Handles abbreviations
        (
            "Dr. Smith is here. He came from the U.S.!",
            ["Dr. Smith is here.", "He came from the U.S.!"],
        ),
        (
            "E.g., this is an example. I.e., it works!",
            ["E.g., this is an example.", "I.e., it works!"],
        ),
        # Edge cases: no splitting after abbreviations
        (
            "Prof. Smith wrote a paper. It was on A.I.",
            ["Prof. Smith wrote a paper.", "It was on A.I."],
        ),
        (
            "U.K. is beautiful. I want to visit!",
            ["U.K. is beautiful.", "I want to visit!"],
        ),
        # Complex punctuation
        ("Wait... what? Really?!", ["Wait... what?", "Really?!"]),
        ("He said, 'Hello!' and left.", ["He said, 'Hello!' and left."]),
        # No sentences
        ("", []),
        ("   ", []),
        # Single sentence
        ("This is a single sentence.", ["This is a single sentence."]),
    ],
)
def test_custom_sent_tokenize(text, expected):
    assert custom_sent_tokenize(text) == expected


@pytest.mark.parametrize(
    "text, expected",
    [
        # Titles
        (
            "Dr. Smith went to see Prof. Johnson. They had a meeting.",
            ["Dr. Smith went to see Prof. Johnson.", "They had a meeting."],
        ),
        (
            "Rev. Carter visited St. Mary's Church.",
            ["Rev. Carter visited St. Mary's Church."],
        ),
        # Latin phrases
        (
            "E.g., this is an example. I.e., it works as intended.",
            ["E.g., this is an example.", "I.e., it works as intended."],
        ),
        (
            "Many people use etc. in lists. It means 'and so on.'",
            ["Many people use etc. in lists.", "It means 'and so on.'"],
        ),
        # Places
        (
            "The U.S. is a large country. The U.K. is smaller.",
            ["The U.S. is a large country.", "The U.K. is smaller."],
        ),
        (
            "Meet me at 3 P.M. in the E.U. headquarters.",
            ["Meet me at 3 P.M. in the E.U. headquarters."],
        ),
        # Miscellaneous
        (
            "Acme Co. is expanding. Fig. 3 shows the growth curve.",
            ["Acme Co. is expanding.", "Fig. 3 shows the growth curve."],
        ),
        (
            "Vol. 4 was released yesterday. It's an improvement over Vol. 3.",
            ["Vol. 4 was released yesterday.", "It's an improvement over Vol. 3."],
        ),
        # Edge cases
        (
            "This is a test... Wait, what? Really?!",
            ["This is a test...", "Wait, what?", "Really?!"],
        ),
        (
            "The price is approx. $50. It's not exact.",
            ["The price is approx. $50.", "It's not exact."],
        ),
        (
            "Dr. Smith, et al., published a paper. It was groundbreaking.",
            ["Dr. Smith, et al., published a paper.", "It was groundbreaking."],
        ),
    ],
)
def test_custom_sent_tokenize_extended(text, expected):
    assert custom_sent_tokenize(text) == expected
