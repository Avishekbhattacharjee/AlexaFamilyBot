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

async def download_from_url(url: str, file_name: str) -> str:
    """
    Download files from URL
    """
    start = datetime.now()
    downloader = Downloader(url=url)
    if downloader.is_running:
        sleep(1)
    end = datetime.now()
    duration = (end - start).seconds
    os.rename(downloader.file_name, file_name)
    status = f"Downloaded `{file_name}` in {duration} seconds."
    return status

async def download_from_tg(target_file) -> (str, BytesIO):
    """
    Download files from Telegram
    """
    async def dl_file(buffer: BytesIO) -> BytesIO:
        buffer = await target_file.client.download_media(
            reply_msg,
            buffer)
        return buffer
    start = datetime.now()
    buf = BytesIO()
    reply_msg = await target_file.get_reply_message()
    avail_mem = psutil.virtual_memory().available + psutil.swap_memory().free
    try:
        if reply_msg.media.document.size >= avail_mem:  # unlikely to happen but baalaji crai
            filen = await target_file.client.download_media(
                reply_msg)
        else:
            buf = await dl_file(buf)
            filen = reply_msg.media.document.attributes[0].file_name
    except AttributeError:
        buf = await dl_file(buf)
        try:
            filen = reply_msg.media.document.attributes[0].file_name
        except AttributeError:
            if isinstance(reply_msg.media, MessageMediaPhoto):
                filen = 'photo-' + str(datetime.today())\
                    .split('.')[0].replace(' ', '-') + '.jpg'
            else:
                filen = reply_msg.media.document.mime_type\
                    .replace('/', '-' + str(datetime.now())
                             .split('.')[0].replace(' ', '-') + '.')
    end = datetime.now()
    duration = (end - start).seconds
    await target_file.reply(f"Downloaded `{filen}` in `{duration}` seconds.")
    return filen, buf



@register(pattern=r"^/download(?: |$)(.*)")
async def download(target_file):
    """ For .download command, download files to the userbot's server. """
    if target_file.fwd_from:
        return
    loma = await target_file.reply("Processing ...")
    input_str = target_file.pattern_match.group(1)
    reply_msg = await target_file.get_reply_message()
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if reply_msg and reply_msg.media:
        await loma.edit("Downloading file from Telegram....")
        filen, buf = await download_from_tg(target_file)
        if buf:
            with open(filen, 'wb') as to_save:
                to_save.write(buf.read())
    elif "|" in input_str:
        url, file_name = input_str.split("|")
        url = url.strip()
        file_name = file_name.strip()
        await loma.edit(f'`Downloading {file_name}`')
        status = await download_from_url(url, file_name)
        await loma.edit(status)
    else:
        await loma.edit("`Reply to a message to \
            download to my local server.`\n")

__help__ = """
*NOTE : all stored files will be automatically purged after 30 minutes !*

FOR DOWNLOADING FILES FROM URL YOU CAN USE TERMINAL USE `/help Terminal` FOR HELP !

 - /download: Type in reply to a telegram document/audio/video to download to the bots local server
"""
__mod_name__ = "Download"
