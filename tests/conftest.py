from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Type

import nonebot
import pytest

if TYPE_CHECKING:
    from nonebot.adapters import Message

config = {
    'strman_respath': Path(__file__).parent / 'testdata',
    'strman_profile': 'test',
}


@pytest.fixture
def setup() -> Iterator[None]:

    nonebot.init(**config)
    nonebot.load_plugin('./nonebot_plugin_styledstr')
    yield
    nbconf = nonebot.get_driver().config
    nbconf.strman_respath = Path(__file__).parent / 'testdata'
    nbconf.strman_profile = 'test'


@pytest.fixture(scope='module')
def parser() -> Iterator[Type['Message']]:

    from utils import FakeMessage

    nonebot.init(**config)
    nonebot.load_plugin('./nonebot_plugin_strman')

    _parser = nonebot.require('nonebot_plugin_strman').init(FakeMessage)
    yield _parser
