import pytest

from utils import make_fake_message

Message = make_fake_message()


def test_export_default(setup) -> None:
    """测试以默认配置创建解析器对象。"""

    from nonebot import require

    parser = require("nonebot_plugin_strman").init(Message)
    assert parser("test.dirname") == Message("test.yaml")


def test_export_with_extra_attr_config(setup) -> None:
    """测试以传入关键字参数设置额外配置创建解析器对象。"""

    from nonebot import require

    parser = require("nonebot_plugin_strman").init(
        Message,
        respath="tests/testdata/load",
        profile="load",
    )
    assert parser("test.dirname") == Message("load/load.yaml")


def test_export_with_extra_dict_config(setup) -> None:
    """测试以传入字典设置额外配置创建解析器对象。"""

    from nonebot import require

    config = {
        "strman_respath": "tests/testdata/load",
        "strman_profile": "load",
    }

    parser = require("nonebot_plugin_strman").init(Message, config=config)
    assert parser("test.dirname") == Message("load/load.yaml")


def test_export_with_modify_nb_config(setup) -> None:
    """测试以修改 NoneBot 配置创建解析器对象。"""

    import nonebot

    config = nonebot.get_driver().config
    config.strman_respath = "tests/testdata/load"
    config.strman_profile = "load"

    parser = nonebot.require("nonebot_plugin_strman").init(Message)
    assert parser("test.dirname") == Message("load/load.yaml")


def test_export_without_message_impl(setup) -> None:
    """测试以非 Message 实现包装创建解析器对象。"""

    from nonebot import require

    parser = require("nonebot_plugin_strman").init()
    result = parser("test.dirname")
    assert isinstance(result, str)
    assert result == "test.yaml"


def test_export_with_unexpected_config(setup) -> None:
    """测试传入非预期的 `config` 参数。"""

    from nonebot import require

    with pytest.raises(ValueError):
        require("nonebot_plugin_strman").init(Message, config="config")
