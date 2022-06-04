from typing import List, Optional

from nonebot import get_driver
from pydantic import BaseSettings


class Config(BaseSettings):
    anti_flash_send_image: bool = False
    anti_flash_send_self: bool = False
    anti_flash_send_user: List[int] = []
    anti_flash_send_group: List[int] = []
    anti_flash_save_folder: Optional[str] = None
    anti_flash_access_address: Optional[str] = None

    class Config:
        extra = "ignore"


global_config = get_driver().config
plugin_config = Config(**global_config.dict())
