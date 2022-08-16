"""字符串管理"""
from importlib.metadata import version
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, Union

from nonebot.config import Config as NBConfig
from nonebot.log import logger
from nonebot.plugin.export import export

from .parser import Parser

if TYPE_CHECKING:
    from nonebot.adapters import Message

__version__ = version("nonebot_plugin_strman")
logger.success(f"Plugin loaded: <b>NoneBot String Manager v{__version__}</b>")


@export()
def init(
    impl: Optional[Type["Message"]] = None,
    **config: Union[NBConfig, Dict[str, Any], str],
) -> Parser:
    """
    创建解析器对象。

    参数：
    - `impl: Optional[Union[Type[Message]]]`：消息实现；
    - `**config: Union[nonebot.config.Config, Dict[str, Any], str]`：插件配置。

    返回：
    - `parser.Parser`：解析器对象。
    """
    if not config:
        parser = Parser(impl)
    elif _config := config.pop("config", None):
        if isinstance(_config, dict):
            parser = Parser(impl, **_config)
        elif isinstance(_config, NBConfig):
            parser = Parser(impl, **_config.dict())
        else:
            raise ValueError("Invalid config type")
    else:
        conf_attr = {
            "strman_respath": config.pop("respath", None),
            "strman_profile": config.pop("profile", None),
        }
        parser = Parser(impl, **{k: v for k, v in conf_attr.items() if v is not None})

    return parser
