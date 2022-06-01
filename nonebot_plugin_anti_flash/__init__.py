import os
import pathlib
import re
import time

import httpx
from nonebot import on_message, logger
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
)
from nonebot.params import Depends

from .config import plugin_config

FILE = re.compile(r"file=(.*?)\.image.*type=flash", re.S)


async def get_client() -> httpx.AsyncClient:
    async with httpx.AsyncClient() as client:
        yield client


anti_flash_matcher = on_message(priority=1, block=False)


@anti_flash_matcher.handle()
async def _(
    bot: Bot, event: MessageEvent, client: httpx.AsyncClient = Depends(get_client)
):
    message = str(event.get_message())
    msg0 = event.get_message()[0]
    if message.startswith("&#91;") and message.endswith("&#93;"):  # go-cq issue
        imgid: str = FILE.findall(message)[0]
    elif msg0.type == "image" and "type" in msg0.data and msg0.data["type"] == "flash":
        imgid: str = msg0.data["file"].rstrip(".image")
    else:
        return  # This is not a flash image

    url = f"https://gchat.qpic.cn/gchatpic_new//--{imgid.upper()}/0"

    mss = []
    if isinstance(event, GroupMessageEvent):
        mss.append(MessageSegment.text(f"Group {event.group_id}\n"))
    mss.append(MessageSegment.text(f"User {event.user_id}\n"))
    mss.append(MessageSegment.text(f"Raw link {url}\n"))
    mss.append(MessageSegment.text(f"Time {time.strftime('%Y-%m-%d %H:%M:%S')}\n"))
    if plugin_config.anti_flash_send_image:
        mss.append(MessageSegment.image(url))

    if plugin_config.anti_flash_send_self:
        await bot.send_private_msg(user_id=bot.self_id, message=Message(mss))

    for user in plugin_config.anti_flash_send_user:
        await bot.send_private_msg(user_id=user, message=Message(mss))

    for group in plugin_config.anti_flash_send_group:
        await bot.send_group_msg(group_id=group, message=Message(mss))

    if plugin_config.anti_flash_save_folder:
        from .utils import save_image_from_url

        path = pathlib.Path(plugin_config.anti_flash_save_folder)

        if isinstance(event, GroupMessageEvent):
            path = path / "group" / f"{event.group_id}"
        else:
            path = path / "private" / f"{event.user_id}"

        if not path.exists():
            os.mkdir(path.resolve())

        await save_image_from_url(
            url,
            path=path,
            filename=f"{event.user_id}-{imgid}",
            client=client,
        )


# Create folder for saving image
if plugin_config.anti_flash_save_folder:
    path = pathlib.Path(plugin_config.anti_flash_save_folder)
    if not path.exists():
        try:
            os.mkdir(path.resolve())
        except FileNotFoundError as e:
            logger.error(
                f"Fail to create folder at {path.resolve()}, please create it by your self."
            )
            raise

    group = path / "group"
    private = path / "private"

    if not group.exists():
        os.mkdir(group.resolve())

    if not private.exists():
        os.mkdir(private.resolve())
