"""字符串管理解析器"""
import importlib.util
import json
import random
from functools import reduce
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, Union

import nonebot
import yaml
from nonebot.log import logger

from .config import Config

if TYPE_CHECKING:
    from nonebot.adapters import Bot, Message


class Parser(object):
    """
    字符串标签解析器。

    属性：
    - `respath`：字符串预设文件资源目录；
    - `profile`：字符串预设文件名称；
    - `message`：NoneBot 适配器对应 `Message` 实现。
    """

    def __init__(self, bot: Type['Bot'], **config: Any) -> None:
        """
        解析器初始化。
        
        参数：
        - `bot: Type[Bot]`：Bot 对象；
        - `**config: Any`：配置参数。
        """
        init_conf = nonebot.get_driver().config.dict()
        if config:
            init_conf.update(config)

        conf = Config(**init_conf)

        self.respath = conf.strman_respath
        self.profile = conf.strman_profile
        self.message = self._get_message_impl(bot)

    def parse(self,
              tag: str,
              /,
              *args: Any,
              profile: Optional[str] = None,
              **kwargs: Any) -> 'Message':
        """
        解析字符串标签获取内容。
        
        参数：
        - `tag: str`：字符串标签；
        - `profile: Optional[str]`：字符串预设文件名称，默认为 `STRMAN_PROFILE`
          所指定的默认预设配置；
        - `*args, **kwargs: Any`：替换内容。
        
        返回：
        - `Message`：被对应适配器的 `Message` 对象包装的解析内容。
        """
        profile = profile if profile else self.profile

        profile_data = self._load_profile(profile)
        raw = self._tag_parse(tag, profile_data)

        return self.message.template(raw).format(*args, **kwargs)

    @staticmethod
    def _get_message_impl(bot: Type['Bot']) -> Type['Message']:
        """
        获取 bot 对应适配器的消息实现。

        参数：
        - `bot: Type[Bot]`：Bot 对象。

        异常：
        - `ValueError`：适配器不存在，或因适配器未安装，或获得的适配器名无效。

        返回：
        - `Type[Message]`：适配器消息实现。
        """
        adapter: str = bot.type.lower().replace(' ', '.')  # type: ignore
        spec = importlib.util.find_spec(f'nonebot.adapters.{adapter}.message')

        if spec is not None:
            module = importlib.util.module_from_spec(spec)
            loader = spec.loader
            if loader is not None:
                loader.exec_module(module)
                logger.debug(f'Loaded {adapter} message module.')
                return module.Message

        raise ValueError(f'Adapter {adapter} not found. Maybe the adapter is '
                         'not installed, or the adapter is invalid.')

    @staticmethod
    def _tag_parse(tag: str, contents: Dict[str, Any]) -> str:
        """
        解析字符串标签。

        参数：
        - `tag: str`：字符串标签。
        - `contents: Dict[str, Any]`：字符串预设内容。

        异常：
        - `KeyError`：字符串标签不存在；
        - `TypeError`：字符串标签内容类型错误。
        
        返回：
        - `str`：标签所指示的字符串内容。特别地，当 `contents` 中标签所对应的内
          容为多个时，则从中随机抽取值返回。
        """
        try:
            result: Any = reduce(lambda key, val: key[val], tag.split('.'),
                                 contents)
        except KeyError as err:
            raise KeyError(f'Tag {tag} is invalid.') from err
        else:
            if isinstance(result, list):
                if not any(isinstance(item, (dict, list)) for item in result):
                    return random.choice(result)
            elif isinstance(result, (str, int, float, bool)):
                return str(result)
            raise TypeError(
                f'The content of tag {tag} is with unsupported type.')

    def _load_profile(self, profile: Union[str, Path]) -> Dict[str, Any]:
        """
        加载字符串预设文件。

        参数：
        - `profile: Union[str, pathlib.Path]`：字符串预设文件。
          - 当 `profile` 为包含预设文件扩展名的字符串或 `pathlib.Path` 文件对象
            时，则将 `profile` 视为预设文件，尝试直接加载；
          - 当 `profile` 为不包含预设文件扩展名的字符串时，`profile` 将被视为预
            设名称，此时将在 `STRMAN_RESPATH` 默认资源目录下检索预设文件；
          - 当 `profile` 为 `pathlib.Path` 目录对象时，资源目录将被其临时覆盖，
            此时将在该目录下检索由 `STRMAN_PROFILE` 所指定的默认预设文件。

        异常：
        - `FileNotFoundError`：字符串预设文件不存在。

        返回：
        - `Dict[str, Any]`：字符串预设文件内容。
        """
        accept_ext = {'.json', '.yml', '.yaml'}

        is_profile_file = (Path(profile).is_file()
                           and Path(profile).suffix in accept_ext)

        if is_profile_file:
            profile_file = Path(profile)
        else:
            file_dir = profile if isinstance(profile, Path) else self.respath
            name = profile if isinstance(profile, str) else self.profile

            files = [file for file in file_dir.iterdir() if file.stem == name]

            if not files:
                raise FileNotFoundError(f'Profile {name} not found.')

            profile_file = sorted(files)[0]

        with profile_file.open(encoding='utf-8') as file:
            if profile_file.suffix == '.json':
                loaded = json.load(file)
            else:
                loaded = yaml.safe_load(file)

        return loaded
