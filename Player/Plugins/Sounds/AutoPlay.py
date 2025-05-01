import asyncio
from pyrogram import filters
from Player import app
from Player.Misc import SUDOERS
from Player.Utils.AutoPlay import autoplay
import config
from pyrogram.enums import ChatMembersFilter


AUTOPLAY_COMMAND = ["AP", "AUTOPLAY"]
PREFIX = config.PREFIX
RPREFIX = config.RPREFIX

@app.on_message((filters.command(AUTOPLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _autoplay(_, message):
    chat_id = message.chat.id
    admins = []
    async for admin in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        admins.append(admin.user.id)
    if message.from_user.id in SUDOERS or message.from_user.id in admins:
        autoplay_status = await autoplay(chat_id)
        status = "ON" if autoplay_status else "OFF"
        await app.send_message(chat_id, f"**AUTOPLAY {status}.\n\n **Now Song Will Play After No Song In Queue**")
    else:
        await app.send_message(chat_id, "**You Don't Have Permission To Set AUTOPLAY**")
