"""字符串管理"""
from importlib.metadata import version
from typing import Any, Dict, Optional, Type, Union

from nonebot.adapters import Bot
from nonebot.config import Config as NBConfig
from nonebot.log import logger
from nonebot.plugin.export import export

from .parser import Parser

__version__ = version('nonebot_plugin_strman')

logger.info(f'Plugin loaded: nonebot_plugin_strman v{__version__}')


@export()
def init(bot: Type[Bot],
         config: Optional[Union[NBConfig, Dict[str, Any]]] = None) -> Parser:
    """
    创建解析器对象。

    参数：
    - `bot: Type[Bot]`：Bot 对象；
    - `config: Optional[Union[nonebot.config.Config, Dict[str, Any]]]`：
      插件配置。

    返回：
    - `parser.Parser`：解析器对象。
    """
    if not config:
        parser = Parser(bot)
    elif isinstance(config, dict):
        parser = Parser(bot, **config)
    else:
        parser = Parser(bot, **config.dict())

    return parser
