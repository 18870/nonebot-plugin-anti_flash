import re
import time

from nonebot import on_message
from nonebot.adapters.onebot.v11 import (
    Bot,
    GroupMessageEvent,
    Message,
    MessageEvent,
    MessageSegment,
)

from .config import plugin_config

FILE = re.compile(r"file=(.*?).image", re.S)

anti_flash_matcher = on_message(priority=1, block=False)


@anti_flash_matcher.handle()
async def _(bot: Bot, event: MessageEvent):
    message = str(event.get_message())
    if message.startswith("&#91;") and message.endswith("&#93;"):
        imgid: str = FILE.findall(message)[0]
    else:
        return  # This is not a flash image

    url = f"https://gchat.qpic.cn/gchatpic_new//--{imgid.upper()}/0"

    mss = []
    if isinstance(event, GroupMessageEvent):
        mss.append(MessageSegment.text(f"Group {event.group_id}\n"))
    mss.append(MessageSegment.text(f"User {event.user_id}\n"))
    mss.append(MessageSegment.text(f"Link {url}\n"))
    mss.append(MessageSegment.text(f"Time {time.strftime('%Y-%m-%d %H:%M:%S')}"))
    mss.append(MessageSegment.image(url))

    if plugin_config.anti_flash_send_self:
        await bot.send_private_msg(user_id=bot.self_id, message=Message(mss))

    for user in plugin_config.anti_flash_send_user:
        await bot.send_private_msg(user_id=user, message=Message(mss))

    for group in plugin_config.anti_flash_send_group:
        await bot.send_group_msg(group_id=group, message=Message(mss))
