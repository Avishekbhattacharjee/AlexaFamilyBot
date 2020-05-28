import aiohttp
import asyncio
import math
import os
from haruka.events import register
from haruka import TEMP_DOWNLOAD_DIRECTORY
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
            ms = (end - start).seconds
            await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
    elif input_str:
        start = datetime.now()
        url = input_str
        file_name = os.path.basename(url)
        to_download_directory =TEMP_DOWNLOAD_DIRECTORY
        if "|" in input_str:
            url, file_name = input_str.split("|")
        url = url.strip()
        file_name = file_name.strip()
        downloaded_file_name = os.path.join(to_download_directory, file_name)
        downloader = SmartDL(url, downloaded_file_name, progress_bar=False)
        downloader.start(blocking=False)
        c_time = time.time()
        while not downloader.isFinished():
            total_length = downloader.filesize if downloader.filesize else None
            downloaded = downloader.get_dl_size()
            display_message = ""
            now = time.time()
            diff = now - c_time
            percentage = downloader.get_progress() * 100
            speed = downloader.get_speed()
            elapsed_time = round(diff) * 1000
            try:
                current_message = f"trying to download\nURL: {url}\nFile Name: {file_name}\n{progress_str}\n{humanbytes(downloaded)} of {humanbytes(total_length)}\nETA: {estimated_total_time}"
                if round(diff % 10.00) == 0 and current_message != display_message:
                    await mone.edit(current_message)
                    display_message = current_message
            except Exception as e:
                logger.info(str(e))
        end = datetime.datetime.now()
        ms = (end - start).seconds
        if downloader.isSuccessful():
            await mone.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
        else:
            await mone.edit("Incorrect URL\n {}".format(input_str))
    else:
        await mone.edit("Reply to a message to download to my local server.")
__help__ = """
*NOTE : USERS IS YOUR RESPONSIBILITY TO REMOVE YOUR FILES AFTER USAGE SHOW THE BOT'S STORAGE DOES NOT GET FULL USE `term rm -r yourfilename` TO REMOVE YOUR FILE/AUDIO/VIDEO FROM THE LOCAL STORAGE*

*NOTE: IF YOU FIND THAT THE BOT ISN'T DOWNLOADING FILES IT MEANS THE BOT'S STORAGE IS FULL JUST TYPE `rm -rf /Downloads` TO FIX IT !*

 - /download: Type in reply to a telegram document/audio/video to download to the bots local server
 - /download <url> | <filename>: Download a file from urlband stores into the bot's local server
"""
__mod_name__ = "Download"
