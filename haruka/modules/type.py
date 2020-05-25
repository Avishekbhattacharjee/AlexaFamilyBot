import random
import re
import time
from cowpy import cow
from haruka.events import register
import html
import random
import time
from typing import List

from telegram import Bot, Update, ParseMode
from telegram.ext import run_async

from haruka import dispatcher
from haruka.modules.helper_funcs.chat_status import is_user_admin, user_admin
from haruka.modules.helper_funcs.extraction import extract_user


@register(pattern='^/type(?: |$)(.*)')
async def typewriter(typew):
    """ Just a small command to make your keyboard become a typewriter! """
    textx = await typew.get_reply_message()
    message = typew.pattern_match.group(1)
    if message:
        pass
    elif textx:
        message = textx.text
    else:
        await typew.reply("`Give a text to type!`")
        return
    sleep_time = 0.03
    typing_symbol = "|"
    old_text = ''
    await typew.edit_text(typing_symbol)
    await asyncio.sleep(sleep_time)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await typew.edit_text(typing_text)
        await asyncio.sleep(sleep_time)
        await typew.edit_text(old_text)
        await asyncio.sleep(sleep_time)


__help__ = """
 - /type <text>: Make the bot type something for you in a professional way 
"""
__mod_name__ = "Typewriter"
