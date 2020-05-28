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
    else:
       await event.reply("Reply to a file/audio/video to download to my local storage")


@register(pattern="^/downloadurl (.*)")
async def _(event):
    if event.fwd_from:
        return
    input_str = event.pattern_match.group(1)
    start = datetime.datetime.now()
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
      joba = await event.reply("Processing ...")
      end = datetime.datetime.now()
      ms = (end - start).seconds
      if downloader.isSuccessful():
         await joba.edit("Downloaded to `{}` in {} seconds.".format(downloaded_file_name, ms))
      else:
         await joba.edit("Incorrect URL\n {}".format(input_str))
    

__help__ = """
NOTE : USERS IS YOUR RESPONSIBILITY TO REMOVE YOUR FILES AFTER USAGE SHOW THE BOT'S STORAGE DOES NOT GET FULL USE `/term cd /Downloads && rm -r yourfilename` TO REMOVE YOUR FILE/AUDIO/VIDEO FROM THE LOCAL STORAGE

NOTE: IF YOU FIND THAT THE BOT ISN'T DOWNLOADING FILES IT MEANS THE BOT'S STORAGE IS FULL JUST TYPE `rm -rf /Downloads` TO FIX IT !

 - /download: Type in reply to a telegram document/audio/video to download to the bots local server
 - /downloadurl <url> | <filename>: Download a file from urlband stores into the bot's local server
"""
__mod_name__ = "Download"
