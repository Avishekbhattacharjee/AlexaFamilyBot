import asyncio
import os
import subprocess
import time
import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from telethon import events
from telethon.tl.types import DocumentAttributeVideo
from telethon.tl.types import DocumentAttributeAudio
from haruka.events import register
from haruka import TEMP_DOWNLOAD_DIRECTORY

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
        start = datetime.datetime.now()
        c_time = time.time()
        await event.client.send_file(
            event.chat_id,
            input_str,
            force_document=True,
            supports_streaming=False,
            allow_cache=False,
            reply_to=event.message.id,
            thumb=thumb)
        end = datetime.datetime.now()
        os.remove(input_str)
        ms = (end - start).seconds
        await mone.edit("Uploaded in {} seconds.".format(ms))
    else:
        await mone.edit("File Not Found")


def get_video_thumb(file, output=None, width=90):
    metadata = extractMetadata(createParser(file))
    p = subprocess.Popen([
        'ffmpeg', '-i', file,
        '-ss', str(int((0, metadata.get('duration').seconds)[metadata.has('duration')] / 2)),
        '-filter:v', 'scale={}:-1'.format(width),
        '-vframes', '1',
        output,
    ], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if not p.returncode and os.path.lexists(file):
        return output


@register(pattern="^/uploadmedia (.*)")
async def _(event):
    if event.fwd_from:
        return
    mone = await event.reply("Processing ...")
    input_str = event.pattern_match.group(1)
    thumb = None
    file_name = input_str
    if os.path.exists(file_name):
        if not file_name.endswith((".mkv", ".mp4", ".mp3", ".flac")):
            await mone.edit(
                "Sorry. But I don't think {} is a streamable file.".format(file_name) + \
                " Please try again.\n" + \
                "**Supported Formats**: MKV, MP4, MP3, FLAC"
            )
            return False
        if os.path.exists(thumb_image_path):
            thumb = thumb_image_path
        else:
            thumb = get_video_thumb(file_name, thumb_image_path)
        start = datetime.datetime.now()
        metadata = extractMetadata(createParser(file_name))
        duration = 0
        width = 0
        height = 0
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        if os.path.exists(thumb_image_path):
            metadata = extractMetadata(createParser(thumb_image_path))
            if metadata.has("width"):
                width = metadata.get("width")
            if metadata.has("height"):
                height = metadata.get("height")
        # Telegram only works with MP4 files
        # this is good, since with MKV files sent as streamable Telegram responds,
        # Bad Request: VIDEO_CONTENT_TYPE_INVALID
        c_time = time.time()
        try:
            await event.client.send_file(
                event.chat_id,
                file_name,
                thumb=thumb,
                caption=input_str,
                force_document=False,
                allow_cache=False,
                reply_to=event.message.id,
                attributes=[
                    DocumentAttributeVideo(
                        duration=duration,
                        w=width,
                        h=height,
                        round_message=False,
                        supports_streaming=True)
                ])
        except Exception as e:
            await mone.edit(str(e))
        else:
            end = datetime.datetime.now()
            os.remove(input_str)
            ms = (end - start).seconds
            await mone.edit("Uploaded in {} seconds.".format(ms))
    else:
        await mone.edit("404: File Not Found")

@register(pattern="^/lsdownloads")
async def _(event):
    if event.fwd_from:
        return
    os.chdir('/root/Downloads')
    lmao = os.system(ls)
    desi = print(lmao)
    await event.reply(desi)
    

__help__ = """
 - /upload <file name>: uploads the downloaded file inside Alexa's cloud storage to telegram

*TO LIST ALL THE DOWNLOADS(THIS INCLUDES EVERYONE'S FILES SO BETTER DON'T STORE PRIVATE FILES TO THE BOT STORAGE):

 - /lsdownloads: lists all the downloaded files of AlexaFamilyBot
"""
__mod_name__ = "Upload"
