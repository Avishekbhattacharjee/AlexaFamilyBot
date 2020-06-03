import asyncio
from datetime import datetime
import io
import os
import requests
from telethon import events
from haruka.events import register
from haruka import REM_BG_API_KEY, TEMP_DOWNLOAD_DIRECTORY

@register(pattern="^/rmbg (.*)")
async def _(event):
    HELP_STR = "use `/rmbg` as reply to a media"
    if event.fwd_from:
        return
    if REM_BG_API_KEY is None:
        await event.reply("You need API token from remove.bg to use this plugin.")
        return False
    input_str = event.pattern_match.group(1)
    start = datetime.now()
    message_id = event.message.id
    if event.reply_to_msg_id:
        message_id = event.reply_to_msg_id
        reply_message = await event.get_reply_message()
        # check if media message
        await event.reply("Downloading this media ...")
        try:
            downloaded_file_name = await event.client.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await event.reply(str(e))
            return
        else:
            await event.reply("sending to ReMove.BG")
            output_file_name = ReTrieveFile(downloaded_file_name)
            os.remove(downloaded_file_name)
    elif input_str:
        await event.reply("sending to ReMove.BG")
        output_file_name = ReTrieveURL(input_str)
    else:
        await event.reply(HELP_STR)
        return
    contentType = output_file_name.headers.get("content-type")
    if "image" in contentType:
        with io.BytesIO(output_file_name.content) as remove_bg_image:
            remove_bg_image.name = "rmbg.png"
            await event.send_file(
                event.chat_id,
                remove_bg_image,
                force_document=True,
                supports_streaming=False,
                allow_cache=False,
                reply_to=message_id
            )
        end = datetime.now()
        ms = (end - start).seconds
        await event.reply("Background Removed in {} seconds".format(ms))
        os.remove(remove_bg_image)
    else:
        await event.reply("ReMove.BG API returned Errors. Please report to @AlexaSupport\n`{}".format(output_file_name.content.decode("UTF-8")))


# this method will call the API, and return in the appropriate format
# with the name provided.
def ReTrieveFile(input_file_name):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    files = {
        "image_file": (input_file_name, open(input_file_name, "rb")),
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        files=files,
        allow_redirects=True,
        stream=True
    )
    return r


def ReTrieveURL(input_url):
    headers = {
        "X-API-Key": REM_BG_API_KEY,
    }
    data = {
      "image_url": input_url
    }
    r = requests.post(
        "https://api.remove.bg/v1.0/removebg",
        headers=headers,
        data=data,
        allow_redirects=True,
        stream=True
    )
    return r

__help__ = """
 - /rmbg: Type in reply to a media to remove it's background 
"""

__mod_name__ = "Remove BG"
