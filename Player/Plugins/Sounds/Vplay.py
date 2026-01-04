"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import time
import asyncio
import config

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter

from Player import app, seek_chats
from Player.Core import Userbot
from Player.Utils.YtDetails import SearchYt, ytdl as Ytdl
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Utils.Delete import delete_messages
from Player.Misc import SUDOERS

# 🔑 Autoplay support
from Player.Plugins.Sounds.Play import last_played_title

PLAY_COMMAND = ["V", "VPLAY"]
PLAYFORCE_COMMAND = ["VPFORCE", "VPLAYFORCE"]

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


# ─────────────────────────────
# PLAY VIDEO (NORMAL)
# ─────────────────────────────
@app.on_message(
    filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])
    & filters.group
)
async def play_video(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = message.from_user.mention

    await message.delete()
    seek_chats.pop(chat_id, None)

    if len(message.command) < 2:
        return await message.reply_text("❌ Give video name.")

    m = await message.reply_text("🔍 Searching video...")
    query = message.text.split(maxsplit=1)[1]

    search_results, yt_url = await SearchYt(query)
    if not search_results:
        return await m.edit("❌ No results found.")

    status, stream_url = await Ytdl(yt_url)
    if not status:
        return await m.edit(stream_url)

    title = search_results[0]["title"]
    duration = search_results[0]["duration"]

    # 🔥 Autoplay fix
    last_played_title[chat_id] = title

    # ───── QUEUE ─────
    if chat_id in QUEUE:
        q = add_to_queue(chat_id, title, duration, stream_url, mention)
        await m.edit(f"**#{q} Added to queue**")
        return asyncio.create_task(delete_messages(message, m))

    # ───── PLAY ─────
    status, text = await Userbot.playVideo(chat_id, stream_url)
    if not status:
        return await m.edit(text)

    add_to_queue(chat_id, title, duration, stream_url, mention)

    await m.edit(
        f"**🎬 Video Playing in VC**\n\n"
        f"**Title:** {title[:25]}\n"
        f"**Duration:** {duration}\n"
        f"**Requested by:** {mention}"
    )
    return asyncio.create_task(delete_messages(message, m))


# ─────────────────────────────
# PLAY FORCE VIDEO (ADMIN)
# ─────────────────────────────
@app.on_message(
    filters.command(PLAYFORCE_COMMAND, [PREFIX, RPREFIX])
    & filters.group
)
async def playforce_video(_, message):
    chat_id = message.chat.id
    mention = message.from_user.mention

    await message.delete()
    seek_chats.pop(chat_id, None)

    if len(message.command) < 2:
        return await message.reply_text("❌ Give video name.")

    admins = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]

    if message.from_user.id not in admins and message.from_user.id not in SUDOERS:
        return await message.reply_text("❌ Only admins can use force play.")

    m = await message.reply_text("⚡ Force playing video...")
    query = message.text.split(maxsplit=1)[1]

    search_results, yt_url = await SearchYt(query)
    if not search_results:
        return await m.edit("❌ No results found.")

    status, stream_url = await Ytdl(yt_url)
    if not status:
        return await m.edit(stream_url)

    title = search_results[0]["title"]
    duration = search_results[0]["duration"]

    last_played_title[chat_id] = title

    QUEUE[chat_id] = [(title, duration, stream_url, mention)]

    status, text = await Userbot.playVideo(chat_id, stream_url)
    if not status:
        return await m.edit(text)

    await m.edit(
        f"**⚡ Force Video Playing**\n\n"
        f"**Title:** {title[:25]}\n"
        f"**Duration:** {duration}\n"
        f"**Requested by:** {mention}"
    )
    return asyncio.create_task(delete_messages(message, m))
