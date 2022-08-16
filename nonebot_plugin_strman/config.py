"""插件设置"""
from pathlib import Path

from pydantic import BaseSettings


class Config(BaseSettings):
    """
    插件配置类。

    继承自 pydantic.BaseSettings。
    """

    strman_respath: Path = Path().cwd()
    strman_profile: str = "default"

    class Config(object):
        extra = "ignore"
