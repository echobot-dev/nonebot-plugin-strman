import pytest

from utils import FakeMessage


def test_export_default(setup) -> None:
    """测试以默认配置创建解析器对象。"""

    from nonebot import require

    parser = require('nonebot_plugin_strman').init(FakeMessage)
    assert parser.parse('test.dirname') == FakeMessage('test.yaml')


def test_export_with_extra_attr_config(setup) -> None:
    """测试以传入关键字参数设置额外配置创建解析器对象。"""

    from nonebot import require

    parser = require('nonebot_plugin_strman').init(
        FakeMessage,
        respath='tests/testdata/load',
        profile='load',
    )
    assert parser.parse('test.dirname') == FakeMessage('load/load.yaml')


def test_export_with_extra_dict_config(setup) -> None:
    """测试以传入字典设置额外配置创建解析器对象。"""

    from nonebot import require

    config = {
        'strman_respath': 'tests/testdata/load',
        'strman_profile': 'load',
    }

    parser = require('nonebot_plugin_strman').init(FakeMessage, config=config)
    assert parser.parse('test.dirname') == FakeMessage('load/load.yaml')


def test_export_with_modify_nb_config(setup) -> None:
    """测试以修改 NoneBot 配置创建解析器对象。"""

    import nonebot

    config = nonebot.get_driver().config
    config.strman_respath = 'tests/testdata/load'
    config.strman_profile = 'load'

    parser = nonebot.require('nonebot_plugin_strman').init(FakeMessage)
    assert parser.parse('test.dirname') == FakeMessage('load/load.yaml')


def test_export_without_message_impl(setup) -> None:
    """测试以非 Message 实现包装创建解析器对象。"""

    from nonebot import require

    parser = require('nonebot_plugin_strman').init()
    result = parser.parse('test.dirname')
    assert isinstance(result, str)
    assert result == 'test.yaml'


def test_export_with_unexpected_config(setup) -> None:
    """测试传入非预期的 `config` 参数。"""

    from nonebot import require

    with pytest.raises(ValueError):
        require('nonebot_plugin_strman').init(FakeMessage, config='config')
