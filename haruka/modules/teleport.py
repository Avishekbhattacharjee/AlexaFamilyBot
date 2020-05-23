from io import BytesIO
from time import sleep
from typing import Optional, List
from telegram import TelegramError, Chat, Message
from telegram import Update, Bot, User
from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown
from haruka.modules.helper_funcs.chat_status import is_user_ban_protected, user_admin

import random
import telegram
import haruka.modules.sql.users_sql as sql
from haruka import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, LOGGER
from haruka.modules.helper_funcs.filters import CustomFilters
from haruka.modules.disable import DisableAbleCommandHandler
USERS_GROUP = 4

MESSAGES = (
    "Happy birthday ",
    "Heppi burfdey ",
    "Hep burf ",
    "Happy day of birthing ",
    "Sadn't deathn't-day ",
    "Oof, you were born today ",
)


@run_async
def teleport(bot: Bot, update: Update, args: List[str]):
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError as excp:
        update.effective_message.reply_text("Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), "THIS IS A TELEPORTED MESSAGE SORRY BUT I CAN'T REVAEAL THE SENDER\n\n"+(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text("Couldn't send the message. Perhaps I'm not part of that group?")


__help__ = """
/teleport <chatid> <message>: Teleports a message to a specific chat without revealing the sender.Can even send to DM's but the user must have interacted at least once with the bot !
"""
__mod_name__ = "Teleport"

TELEPORT_HANDLER = DisableAbleCommandHandler("teleport", teleport, pass_args=True)
dispatcher.add_handler(TELEPORT _HANDLER)

