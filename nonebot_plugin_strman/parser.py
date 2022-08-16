"""字符串管理解析器"""
import json
import random
import warnings
from functools import reduce
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Optional, Type, Union

import nonebot
import yaml
from nonebot.log import logger

from .config import Config

if TYPE_CHECKING:
    from nonebot.adapters import Message


class Parser(object):
    """
    字符串标签解析器。

    属性：
    - `respath`：字符串预设文件资源目录；
    - `profile`：字符串预设文件名称；
    - `impl`：NoneBot 适配器对应 `Message` 实现。
    """

    def __init__(self, impl: Optional[Type["Message"]] = None, **config: Any) -> None:
        """
        解析器初始化。

        参数：
        - `impl: Type[Message]`：消息实现；
        - `**config: Any`：配置参数。
        """
        init_conf = nonebot.get_driver().config.dict()
        if config:
            init_conf.update(config)

        conf = Config(**init_conf)

        self.respath = conf.strman_respath
        self.profile = conf.strman_profile
        self.impl = impl

    def __call__(
        self,
        tag: str,
        /,
        *args: Any,
        profile_ol: Optional[str] = None,
        **kwargs: Any,
    ) -> Union["Message", str]:
        """
        解析字符串标签获取内容。

        参数：
        - `tag: str`：字符串标签；
        - `profile_ol: Optional[str]`：重载字符串预设名称，默认遵循
          `STRMAN_PROFILE` 所指定的默认预设配置；
        - `*args, **kwargs: Any`：替换内容。

        返回：
        - `Union[Message, str]`：字符串标签解析内容。指定消息实现时则包装为指定
          的 `Message` 对象，否则返回字符串。
        """
        profile_ol = profile_ol or self.profile

        profile_data = self._load_profile(profile_ol)
        raw = self._tag_parse(tag, profile_data)

        if not self.impl:
            logger.warning(
                "Parsing tag as a string is not recommended, please pass a valid "
                '"Message" implementation while initializing parser to decorate.'
            )
            return raw.format(*args, **kwargs)
        return self.impl.template(raw).format(*args, **kwargs)

    def parse(
        self,
        tag: str,
        /,
        *args: Any,
        profile_ol: Optional[str] = None,
        **kwargs: Any,
    ) -> Union["Message", str]:
        """
        解析字符串标签获取内容。

        此方法将在 v1.2 后弃用，请直接调用实例对象：

        ```python
        >>> parser = Parser(...)
        >>> parser(tag, *args, **kwargs)
        ```
        ---
        参数：
        - `tag: str`：字符串标签；
        - `profile_ol: Optional[str]`：重载字符串预设名称，默认遵循
          `STRMAN_PROFILE` 所指定的默认预设配置；
        - `*args, **kwargs: Any`：替换内容。

        返回：
        - `Union[Message, str]`：字符串标签解析内容。指定消息实现时则包装为指定
          的 `Message` 对象，否则返回字符串。
        """
        warnings.warn(
            (
                "This method is about to be deprecated in v1.2. You should now call "
                "the instance object directly."
            ),
            category=DeprecationWarning,
        )
        return self.__call__(tag, *args, profile_ol=profile_ol, **kwargs)

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
            data: Any = reduce(lambda key, val: key[val], tag.split("."), contents)
        except KeyError as err:
            raise KeyError(f"Tag {tag} is invalid.") from err
        else:
            if isinstance(data, list) and not any(
                isinstance(item, (dict, list)) for item in data
            ):
                logger.debug("Multiple results found. Randomly selected.")
                result = str(random.choice(data))
            elif isinstance(data, (str, int, float, bool)):
                result = str(data)
            else:
                raise TypeError(f"The content of tag {tag} is with unsupported type.")

            logger.info(f"Tag {tag} parsed.")
            return result

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
        accept_ext = {".json", ".yml", ".yaml"}

        if (self.respath / profile).is_file() and Path(profile).suffix in accept_ext:
            profile_file = self.respath / profile
        else:
            file_dir = profile if isinstance(profile, Path) else self.respath
            name = profile if isinstance(profile, str) else self.profile

            if files := [
                file
                for file in file_dir.iterdir()
                if file.stem == name and file.suffix in accept_ext
            ]:
                profile_file = sorted(files)[0]
            else:
                raise FileNotFoundError(f"Profile {name} not found.")

        with profile_file.open(encoding="utf-8") as file:
            if profile_file.suffix == ".json":
                loaded = json.load(file)
            else:
                loaded = yaml.safe_load(file)

        logger.debug(f"Load profile file successfully: {profile_file.absolute()}")
        return loaded
