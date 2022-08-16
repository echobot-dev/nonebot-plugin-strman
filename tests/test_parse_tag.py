from datetime import datetime
from typing import Any, Dict, Tuple, Union

import pytest

from utils import make_fake_message

Message = make_fake_message()
MessageSegment = Message.get_segment_class()


def test_parse_tag(parse) -> None:
    assert parse("tag_value").extract_plain_text() == "Layer 1"


@pytest.mark.parametrize(
    "tag, expected",
    [
        ("tag.value", "Layer 2"),
        ("tag.layer.value", "Layer 3"),
        ("tag.layer.layer.value", "Layer 4"),
    ],
)
def test_parse_hierarchical_tag(parse, tag: str, expected: str) -> None:
    assert parse(tag).extract_plain_text() == expected


def test_parse_tag_with_multiple_values(parse) -> None:
    assert parse("tag_multiple_values").extract_plain_text() in [
        f"value {i}" for i in range(1, 5)
    ]


@pytest.mark.parametrize(
    "tag, args, kwargs, expected",
    [
        (
            "testchamber.keyword",
            (),
            {
                "Subject": "The quick brown fox",
                "ACTION": "jumps over",
                "object": "the lazy dog",
            },
            "The quick brown fox jumps over the lazy dog.",
        ),
        (
            "testchamber.positional",
            ("Prepare for", "unforeseen", "consequences"),
            {},
            "Prepare for unforeseen consequences.",
        ),
        (
            "testchamber.indexed",
            ("can", "canner", "Can"),
            {},
            "Can you can a can as a canner can can a can?",
        ),
        (
            "testchamber.mixed",
            ("positional",),
            {"kw": "keyword"},
            "positional keyword",
        ),
        (
            "testchamber.with_spec",
            (),
            {
                "base": 1,
                "value": 6.3505,
                "provider": "OANDA",
                "date": "Jan 1, 2022",
            },
            (
                "USD 1.00 approx. equals CNY 6.35 (data provided by OANDA on "
                "Jan 1, 2022)."
            ),
        ),
        (
            "testchamber.with_extended_spec",
            (42,),
            {"logo": "file:///path/to/logo.png"},
            (
                MessageSegment.face(42)
                + " "
                + MessageSegment.image("file:///path/to/logo.png")
            ),
        ),
    ],
)
def test_parse_tag_with_format(
    parse,
    tag: str,
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    expected: Union[str, MessageSegment],
) -> None:
    assert (
        parse(tag, *args, **kwargs).extract_plain_text()
        == Message(expected).extract_plain_text()
    )


def test_parse_tag_with_deprecated_method(parse) -> None:
    with pytest.deprecated_call():
        assert parse.parse("tag_value").extract_plain_text() == "Layer 1"
