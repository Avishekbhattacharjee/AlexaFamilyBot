import random
import re
import asyncio
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


@register(pattern="^/type (.*)")
async def typewriter(typew):
    message = typew.pattern_match.group(1)
    if message:
        pass
    else:
        await typew.reply("`Give a text to type!`")
        return
    typing_symbol = "|"
    old_text = ''
    now = await typew.reply(typing_symbol)
    await asyncio.sleep(2)
    for character in message:
        old_text = old_text + "" + character
        typing_text = old_text + "" + typing_symbol
        await now.edit(typing_text)
        await asyncio.sleep(2)
        await now.edit(old_text)
        await asyncio.sleep(2)


__help__ = """
 - /type <text>: Make the bot type something for you in a professional way
"""
__mod_name__ = "Typewriter"
