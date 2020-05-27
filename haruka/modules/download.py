import aiohttp
import asyncio
import math
import os
from haruka import register, TEMP_DOWNLOAD_DIRECTORY
import time
import datetime
from telethon import events
from telethon.tl.types import DocumentAttributeVideo


@register(pattern="^/download")
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    if event.reply_to_msg_id:
        start = datetime.datetime.now()
        reply_message = await event.get_reply_message()
        try:
            downloaded_file_name = await event.client.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY)
        except Exception as e:  
            await mone.edit(str(e))
        else:
            end = datetime.datetime.now()
            ms = (end - start).seconds
            await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))

__help__ = """
 - /download: Type in reply to a telegram document/audio/video to download to the bots local server
"""
__mod_name__ = True
