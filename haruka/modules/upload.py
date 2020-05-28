import asyncio
import os
import subprocess
import time
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from telethon.tl.types import DocumentAttributeAudio
from haruka.events import register
from haruka import TEMP_DOWNLOAD_DIRECTORY
import aiohttp
import asyncio
import math
import os
from pySmartDL import SmartDL
from haruka.events import register
from haruka import TEMP_DOWNLOAD_DIRECTORY
import time
from datetime import datetime
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from io import BytesIO
from time import sleep
import psutil
import subprocess
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from pyDownload import Downloader
from telethon.tl.types import DocumentAttributeVideo, MessageMediaPhoto
import json
import logging
import re

@register(pattern=r"^/upload (.*)")
async def upload(u_event):
    """ For .upload command, allows you to \
    upload a file from the userbot's server """
    if u_event.fwd_from:
        return
    if u_event.is_channel and not u_event.is_group:
        await u_event.reply("Uploading isn't permitted on channels")
        return
    lmao = await u_event.reply("Processing ...")
    input_str = u_event.pattern_match.group(1)
    if os.path.exists(input_str):
        start = datetime.now()
        await u_event.client.send_file(
            u_event.chat_id,
            input_str,
            force_document=True,
            allow_cache=False,
            reply_to=u_event.message.id)
        end = datetime.now()
        duration = (end - start).seconds
        await lmao.edit("Uploaded in {} seconds.".format(duration))
    else:
        await lmao.edit("404: File Not Found")


__help__ = """
*NOTE: as soon as you upload the the stuff they are all removed from the server !*

 - /upload <file name>: uploads the downloaded file inside Alexa's cloud storage to telegram
"""
__mod_name__ = "Upload"
