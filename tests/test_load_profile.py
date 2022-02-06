from pathlib import Path
from typing import Union

import pytest

from utils import FakeMessage

assets_path = Path(__file__).parent / 'testdata'


@pytest.mark.parametrize('path', [
    assets_path,
    'tests/testdata',
    assets_path.absolute(),
])
@pytest.mark.usefixtures('setup')
def test_load_profile_init(path: Union[str, Path]) -> None:
    """
    测试初始化后根据配置默认加载资源目录下的预设文件。
    
    测试 `STRMAN_RESPATH` 分别为 `pathlib.Path` 对象、目录相对/绝对路径字符串的
    行为。
    """

    from nonebot import require

    config = {'strman_respath': path, 'strman_profile': 'test'}
    parser = require('nonebot_plugin_strman').init(FakeMessage, config=config)

    assert parser.parse('test.dirname') == FakeMessage('test.yaml')


@pytest.mark.parametrize('profile, expected', [
    ('load', 'load/load.yaml'),
    ('json_load.json', 'load/json_load.json'),
    ('../test.yaml', 'test.yaml'),
    ((assets_path / 'load' / 'load.yaml').absolute(), 'load/load.yaml'),
    (assets_path / 'test.yaml', 'test.yaml'),
    (assets_path, 'test.yaml'),
])
@pytest.mark.usefixtures('setup')
def test_load_profile_on_calling(profile: Union[str, Path],
                                 expected: str) -> None:
    """
    测试运行时指定预设文件加载。
    
    测试将参数设置为预设名称、相对/绝对路径字符串、`pathlib.Path` 目录/文件对
    象的行为。
    """

    from nonebot import require

    config = {'strman_respath': assets_path / 'load'}
    parser = require('nonebot_plugin_strman').init(FakeMessage, config=config)

    assert parser.parse('test.dirname',
                        profile_ol=profile) == FakeMessage(expected)


@pytest.mark.parametrize('respath, expected', [
    (assets_path / 'load' / 'load_json', 'load/load_json/dup.json'),
    (assets_path / 'load' / 'load_yaml', 'load/load_yml/dup.yaml'),
])
@pytest.mark.usefixtures('setup')
def test_load_profile_priority(respath: Path, expected: str) -> None:
    """
    测试指定预设名称在资源目录下存在多个有效文件时的加载优先级处理。
    """

    from nonebot import require

    config = {'strman_respath': respath, 'strman_profile': 'dup'}
    parser = require('nonebot_plugin_strman').init(FakeMessage, config=config)

    assert parser.parse('test.dirname') == FakeMessage(expected)
