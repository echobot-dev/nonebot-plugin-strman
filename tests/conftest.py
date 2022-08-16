from pathlib import Path
from typing import TYPE_CHECKING, Iterator, Type

import nonebot
import pytest

if TYPE_CHECKING:
    from nonebot.adapters import Message

config = {
    "strman_respath": Path(__file__).parent / "testdata",
    "strman_profile": "test",
}


@pytest.fixture
def setup() -> Iterator[None]:
    nonebot.init(**config)
    if not nonebot.get_plugin("nonebot_plugin_strman"):
        nonebot.load_plugin("./nonebot_plugin_strman")
    yield
    nbconf = nonebot.get_driver().config
    nbconf.strman_respath = Path(__file__).parent / "testdata"
    nbconf.strman_profile = "test"


@pytest.fixture(scope="module")
def parse() -> Iterator[Type["Message"]]:
    from utils import make_fake_message

    nonebot.init(**config)
    if not nonebot.get_plugin("nonebot_plugin_strman"):
        nonebot.load_plugin("./nonebot_plugin_strman")

    Message = make_fake_message()

    yield nonebot.require("nonebot_plugin_strman").init(Message)
