from typing import List

from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    anti_flash_send_self: bool = False
    anti_flash_send_user: List[int] = []
    anti_flash_send_group: List[int] = []

    class Config:
        extra = "ignore"


global_config = get_driver().config
plugin_config = Config(**global_config.dict())
