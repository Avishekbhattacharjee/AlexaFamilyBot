from telethon import events
from datetime import datetime, timedelta
from telethon.tl.types import UserStatusEmpty, UserStatusLastMonth, UserStatusLastWeek, UserStatusOffline, UserStatusOnline, UserStatusRecently, ChannelParticipantsKicked, ChatBannedRights
from telethon.tl import functions, types
from time import sleep
import asyncio
from haruka.events import register

@register(pattern="^/kickthefools")
async def _(event):
    if event.fwd_from:
        return
    if event.is_private:
        return False   
    chat = await event.get_chat()
    if not (chat.admin_rights or chat.creator):
            await event.reply("`I am not admin here!`")
            return False
    p = 0
    b = 0
    c = 0
    d = 0
    ee = []
    m = 0
    n = 0
    y = 0
    w = 0
    o = 0
    q = 0
    r = 0
    await event.reply("Searching Participant Lists...")
    async for i in event.client.iter_participants(event.chat_id):
        p = p + 1
        rights = ChatBannedRights(
            until_date=None,
            view_messages=True
        )
        if isinstance(i.status, UserStatusLastMonth):
            m = m + 1
            status, e = await ban_user(event.chat_id, i, rights)
            if not status:
                    try:
                        await event.reply("I need admin priveleges to perform this action!")
                    except:
                        pass
                    ee.append(str(e))
            else:
                    c = c + 1
                    
        if isinstance(i.status, UserStatusLastWeek):
            w = w + 1
            status, e = await ban_user(event.chat_id, i, rights)
            if not status:
                    try:
                        await event.reply("I need admin priveleges to perform this action!")
                    except:
                        pass
                    ee.append(str(e))
            else:
                    c = c + 1
    required_string = "Successfully Kicked **{}** users"
    await event.reply(required_string.format(c))
        
async def ban_user(chat_id, i, rights):
    try:
        await event.client(functions.channels.replyBannedRequest(chat_id, i, rights))
        return True, None
    except Exception as exc:
        return False, str(exc)
