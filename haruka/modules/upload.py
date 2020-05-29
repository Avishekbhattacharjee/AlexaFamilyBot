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

thumb_image_path = TEMP_DOWNLOAD_DIRECTORY + "/thumb_image.jpg"


@register(pattern="^/upload (.*)")
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    input_str = event.pattern_match.group(1)
    thumb = None
    if os.path.exists(thumb_image_path):
        thumb = thumb_image_path
    if os.path.exists(input_str):
        start = datetime.now()
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            input_str,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
            thumb=thumb)
        end = datetime.now()
        os.remove(input_str)
        ms = (end - start).seconds
        await mone.edit("Uploaded in {} seconds.".format(ms))
    else:
        await mone.edit("File Not Found")



__help__ = """
*NOTE: as soon as you upload the the stuff they are all removed from the server !*

 - /upload <file name>: uploads the downloaded file inside Alexa's cloud storage to telegram
"""
__mod_name__ = "Upload"
