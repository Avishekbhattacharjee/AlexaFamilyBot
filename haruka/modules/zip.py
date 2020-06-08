""" command: .compress """

from telethon import events
import asyncio
import zipfile
from pySmartDL import SmartDL
import time
import os
from haruka.events import register
from haruka import TEMP_DOWNLOAD_DIRECTORY

@register(pattern="^/zip")
async def _(event):
    if event.fwd_from:
        return
    if not event.is_reply:
        await event.reply("Reply to a file to compress it.")
        return
    mone = await event.reply("Processing ...")
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.makedirs(TEMP_DOWNLOAD_DIRECTORY)
    if event.reply_to_msg_id:
        reply_message = await event.get_reply_message()
        try:
            c_time = time.time()
            downloaded_file_name = await event.client.download_media(
                reply_message,
                TEMP_DOWNLOAD_DIRECTORY)
            directory_name = downloaded_file_name
            await event.reply(downloaded_file_name)
        except Exception as e:  # pylint:disable=C0103,W0703
            await mone.reply(str(e))
    zipfile.ZipFile(directory_name + '.zip', 'w', zipfile.ZIP_DEFLATED).write(directory_name)
    await event.client.send_file(
        event.chat_id,
        directory_name + ".zip",
        force_document=True,
        allow_cache=False,
        reply_to=event.message.id,
    )

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))
            os.remove(os.path.join(root, file))
