"""字符串管理"""
from importlib.metadata import version
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, Union

from nonebot.config import Config as NBConfig
from nonebot.log import logger
from nonebot.plugin.export import export

from .parser import Parser

if TYPE_CHECKING:
    from nonebot.adapters import Message

__version__ = version('nonebot_plugin_strman')

logger.info(f'Plugin loaded: nonebot_plugin_strman v{__version__}')


@export()
def init(impl: Optional[Type['Message']] = None,
         config: Optional[Union[NBConfig, Dict[str, Any]]] = None) -> Parser:
    """
    创建解析器对象。

    参数：
    - `impl: Optional[Union[Type[Bot], Type[Message]]]`：适配器实现；
    - `config: Optional[Union[nonebot.config.Config, Dict[str, Any]]]`：
      插件配置。

    返回：
    - `parser.Parser`：解析器对象。
    """
    if not config:
        parser = Parser(impl)
    elif isinstance(config, dict):
        parser = Parser(impl, **config)
    else:
        parser = Parser(impl, **config.dict())

    return parser
