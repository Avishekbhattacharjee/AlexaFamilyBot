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

@register(pattern="^/download")
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        start = datetime.now()
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY)
        except Exception as e: 
            await mone.edit(str(e))
        else:
            end = datetime.now()
            ms = (end - start).seconds
            await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    else:
        await mone.edit("Reply to a message to download to my local server.")


__help__ = """
*NOTE : all stored files will be automatically purged after 30 minutes !*

FOR DOWNLOADING FILES FROM URL YOU CAN USE TERMINAL USE `/help Terminal` FOR HELP !

 - /download: Type in reply to a telegram document/audio/video to download to the bots local server
"""
__mod_name__ = "Download"
