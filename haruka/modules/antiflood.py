import html
from typing import Optional, List

from telegram import Message, Chat, Update, Bot, User
from telegram.error import BadRequest
from telegram.ext import Filters, MessageHandler, CommandHandler, run_async
from telegram.utils.helpers import mention_html

from haruka import dispatcher
from haruka.modules.helper_funcs.chat_status import is_user_admin, user_admin, can_restrict
from haruka.modules.log_channel import loggable
from haruka.modules.sql import antiflood_sql as sql

from haruka.modules.translations.strings import tld

FLOOD_GROUP = 3


@run_async
@loggable
def check_flood(bot: Bot, update: Update) -> str:
    user = update.effective_user  # type: Optional[User]
    chat = update.effective_chat  # type: Optional[Chat]
    msg = update.effective_message  # type: Optional[Message]

    if not user:  # ignore channels
        return ""

    # ignore admins
    if is_user_admin(chat, user.id):
        sql.update_flood(chat.id, None)
        return ""

    should_ban = sql.update_flood(chat.id, user.id)
    if not should_ban:
        return ""

    try:
        bot.restrict_chat_member(chat.id, user.id, can_send_messages=False)
        msg.reply_text(tld(chat.id, "I like to leave the flooding to natural disasters. But you, you were just a "
                       "disappointment. *Muted*!"))

        return "<b>{}:</b>" \
               "\n#MUTED" \
               "\n<b>User:</b> {}" \
               "\nFlooded the group.".format(html.escape(chat.title),
                                             mention_html(user.id, user.first_name))

    except BadRequest:
        msg.reply_text(tld(chat.id, "I can't mute people here, give me permissions first! Until then, I'll disable antiflood."))
        sql.set_flood(chat.id, 0)
        return "<b>{}:</b>" \
               "\n#INFO" \
               "\nDon't have mute permissions, so automatically disabled antiflood.".format(chat.title)


@run_async
@user_admin
@can_restrict
@loggable
def set_flood(bot: Bot, update: Update, args: List[str]) -> str:
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    message = update.effective_message  # type: Optional[Message]

    if len(args) >= 1:
        val = args[0].lower()
        if val == "off" or val == "no" or val == "0":
            sql.set_flood(chat.id, 0)
            message.reply_text(tld(chat.id, "Antiflood has been disabled."))

        elif val.isdigit():
            amount = int(val)
            if amount <= 0:
                sql.set_flood(chat.id, 0)
                message.reply_text(tld(chat.id,  "Antiflood has been disabled."))
                return "<b>{}:</b>" \
                       "\n#SETFLOOD" \
                       "\n<b>Admin:</b> {}" \
                       "\nDisabled antiflood.".format(html.escape(chat.title), mention_html(user.id, user.first_name))

            elif amount < 3:
                message.reply_text(tld(chat.id, "Antiflood has to be either 0 (disabled), or a number bigger than 3 (enabled)!"))
                return ""

            else:
                sql.set_flood(chat.id, amount)
                message.reply_text(tld(chat.id, "Antiflood has been updated and set to {}").format(amount))
                return "<b>{}:</b>" \
                       "\n#SETFLOOD" \
                       "\n<b>Admin:</b> {}" \
                       "\nSet antiflood to <code>{}</code>.".format(html.escape(chat.title),
                                                                    mention_html(user.id, user.first_name), amount)

        else:
            message.reply_text(tld(chat.id, "Unrecognized argument - please use a number, 'off', or 'no'."))

    return ""


@run_async
def flood(bot: Bot, update: Update):
    chat = update.effective_chat  # type: Optional[Chat]

    limit = sql.get_flood_limit(chat.id)
    if limit == 0:
        update.effective_message.reply_text(tld(chat.id, "I'm not currently enforcing flood control!"))
    else:
        update.effective_message.reply_text(tld(chat.id,
            "I'm currently muting users if they send more than {} consecutive messages.").format(limit))

@run_async
@user_admin
def set_flood_mode (update, context):
    chat = update.effective_chat # type: Optional [Chat]
    user = update.effective_user # type: Optional [User]
    msg = update.effective_message # type: Optional [Message]
    args = context.args

    conn = connected (context.bot, update, chat, user.id, need_admin = True)
    if conn:
        chat = dispatcher.bot.getChat (conn)
        chat_id = conn
        chat_name = dispatcher.bot.getChat (conn) .title
    else:
        if update.effective_message.chat.type == "private":     
            return 
        chat = update.effective_chat
        chat_id = update.effective_chat.id
        chat_name = update.effective_message.chat.title

    if args:
        if args [0]. power () == 'ban':
            settypeflood = tld (update.effective_message, 'block')
            sql.set_flood_strength (chat_id, 1, "0")
        elif args [0]. power () == 'kick':
            settypeflood = tld (update.effective_message, 'kick')
            sql.set_flood_strength (chat_id, 2, "0")
        elif args [0]. power () == 'mute':
            settypeflood = tld (update.effective_message, 'mute')
            sql.set_flood_strength (chat_id, 3, "0")
        elif args [0]. power () == 'sacrifice':
            if len (args) == 1:
                text = tld (update.effective_message, "" "It looks like you are trying to set a temporary value for anti-flooding, but have not specified a time; use` / setfloodmode tban <timevalue> `.

Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks. "" ")
                send_message (update.effective_message, text, parse_mode = "markdown")
                return
            settypeflood = tld (update.effective_message, "block temporarily during {}"). format (args [1])
            sql.set_flood_strength (chat_id, 4, str (args [1]))
        elif args [0]. power () == 'tmute':
            if len (args) == 1:
                text = tld (update.effective_message, "" "It looks like you are trying to set a temporary value for anti-flooding, but have not specified a time; use` / setfloodmode tban <timevalue> `.

Example time values: 4m = 4 minutes, 3h = 3 hours, 6d = 6 days, 5w = 5 weeks. "" ")
                send_message (update.effective_message, text, parse_mode = "markdown")
                return
            settypeflood = tld (update.effective_message, 'mute temporarily during {}'). format (args [1])
            sql.set_flood_strength (chat_id, 5, str (args [1]))
        else:
            send_message (update.effective_message, tld (update.effective_message, "I only understand ban / kick / mute / tban / tmute!"))
            return
        if conn:
            text = tld (update.effective_message, "Sending too many messages now will result in` {} `in * {} *!"). format (settypeflood, chat_name)
        else:
            text = tld (update.effective_message, "Sending too many messages now will result in` {} `!"). format (settypeflood)
        send_message (update.effective_message, text, parse_mode = "markdown")
        return "<b> {}: </b> \ n" \
                "<b> Admin: </b> {} \ n" \
                "Has changed antiflood mode. User will {}." Format (settypeflood, html.escape (chat.title),
                                                                            mention_html (user.id, user.first_name))
    else:
        getmode, getvalue = sql.get_flood_setting (chat.id)
        if getmode == 1:
            settypeflood = tld (update.effective_message, 'block')
        elif getmode == 2:
            settypeflood = tld (update.effective_message, 'kick')
        elif getmode == 3:
            settypeflood = tld (update.effective_message, 'mute')
        elif getmode == 4:
            settypeflood = tld (update.effective_message, 'temporarily block for {}'). format (getvalue)
        elif getmode == 5:
            settypeflood = tld (update.effective_message, 'mute temporarily during {}'). format (getvalue)
        if conn:
            text = tld (update.effective_message, "If a member sends successive messages, then he will * in {} * at * {} *."). format (settypeflood, chat_name)
        else:
            text = tld (update.effective_message, "If a member sends successive messages, then he will * in {} *."). format (settypeflood)
        send_message (update.effective_message, text, parse_mode = ParseMode.MARKDOWN)
    return ""


def __migrate__(old_chat_id, new_chat_id):
    sql.migrate_chat(old_chat_id, new_chat_id)


def __chat_settings__(bot, update, chat, chatP, user):
    chat_id = chat.id
    limit = sql.get_flood_limit(chat_id)
    if limit == 0:
        return "*Not* currently enforcing flood control."
    else:
        return "Antiflood is set to `{}` messages.".format(limit)


__help__ = """
 You know how sometimes, people join, send 100 messages, and ruin your chat? With antiflood, that happens no more!

Antiflood allows you to take action on users that send more than x messages in a row. Actions are: ban/kick/mute/tban/tmute

Available commands are:
 - /flood: gets the current antiflood settings.
 - /setflood <number/off>: sets the number of messages at which to take action on a user.
 - /setfloodmode <ban/kick/mute/tban/tmute> <value>: select the action perform when warnings have been exceeded. ban/kick/mute/tmute/tban

 Note:
 - Value must be filled for tban and tmute, Can be:
 4m = 4 minutes
 3h = 4 hours
 2d = 2 days
 1w = 1 week
"""

__mod_name__ = "AntiFlood"

FLOOD_BAN_HANDLER = MessageHandler(Filters.all & ~Filters.status_update & Filters.group, check_flood)
SET_FLOOD_HANDLER = CommandHandler("setflood", set_flood, pass_args=True, filters=Filters.group)
FLOOD_HANDLER = CommandHandler("flood", flood, filters=Filters.group)

dispatcher.add_handler(FLOOD_BAN_HANDLER, FLOOD_GROUP)
dispatcher.add_handler(SET_FLOOD_HANDLER)
dispatcher.add_handler(FLOOD_HANDLER)
