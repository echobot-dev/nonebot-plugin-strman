from datetime import datetime
from typing import Any, Dict, Tuple, Union

import pytest

from utils import FakeMessage, FakeMessageSegment


def test_parse_tag(parser) -> None:

    assert parser.parse('tag_value') == FakeMessage('Layer 1')


@pytest.mark.parametrize('tag, expected', [
    ('tag.value', 'Layer 2'),
    ('tag.layer.value', 'Layer 3'),
    ('tag.layer.layer.value', 'Layer 4'),
])
def test_parse_hierarchical_tag(parser, tag: str, expected: str) -> None:

    assert parser.parse(tag) == FakeMessage(expected)


def test_parse_tag_with_multiple_values(parser) -> None:

    assert parser.parse('tag_multiple_values') in [
        FakeMessage(f'value {i}') for i in range(1, 5)
    ]


@pytest.mark.parametrize('tag, args, kwargs, expected', [
    (
        'testchamber.keyword',
        (),
        {
            'Subject': 'The quick brown fox',
            'ACTION': 'jumps over',
            'object': 'the lazy dog'
        },
        'The quick brown fox jumps over the lazy dog.',
    ),
    (
        'testchamber.positional',
        ('Prepare for', 'unforeseen', 'consequences'),
        {},
        'Prepare for unforeseen consequences.',
    ),
    (
        'testchamber.indexed',
        ('can', 'canner', 'Can'),
        {},
        'Can you can a can as a canner can can a can?',
    ),
    (
        'testchamber.mixed',
        ('positional', ),
        {
            'kw': 'keyword'
        },
        'positional keyword',
    ),
    (
        'testchamber.with_spec',
        (),
        {
            'base': 1,
            'value': 6.3505,
            'provider': 'OANDA',
            'date': 'Jan 1, 2022',
        },
        ('USD 1.00 approx. equals CNY 6.35 (data provided by OANDA on '
         'Jan 1, 2022).'),
    ),
    (
        'testchamber.with_extended_spec',
        (42, ),
        {
            'logo': 'file:///path/to/logo.png'
        },
        (FakeMessageSegment.face(42) + ' ' +
         FakeMessageSegment.image('file:///path/to/logo.png')),
    ),
])
def test_parse_tag_with_format(
        parser, tag: str, args: Tuple[Any, ...], kwargs: Dict[str, Any],
        expected: Union[str, FakeMessageSegment]) -> None:

    assert parser.parse(tag, *args, **kwargs) == FakeMessage(expected)
