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
from Player.Utils.YtDetails import SearchYt, ytdl_audio as Ytdl
from Player.Plugins.Start.Spam import spam_check
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Utils.Delete import delete_messages
from Player.Misc import SUDOERS

# 🔑 Autoplay support
last_played_title = {}

PLAY_COMMAND = ["P", "PLAY", "SP", "SPLAY"]
PLAYFORCE_COMMAND = ["PFORCE", "PLAYFORCE"]

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


# ─────────────────────────────
# REPLY AUDIO HANDLER
# ─────────────────────────────
async def processReplyToMessage(message):
    msg = message.reply_to_message
    if msg and (msg.audio or msg.voice):
        m = await message.reply_text("**𝓦𝓪𝓲𝓽... 𝓓𝓸𝔀𝓷𝓵𝓸𝓪𝓭𝓲𝓷𝓰 ❤️**")
        file_path = await msg.download()
        return file_path, m
    return None, None


# ─────────────────────────────
# PLAY COMMAND (NORMAL)
# ─────────────────────────────
@app.on_message(
    filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])
    & filters.group
    & spam_check()
)
async def play_music(_, message):
    # 🔥 IMPORTANT FIX: playforce exclusion
    if message.command[0].lower() in ["playforce", "pforce"]:
        return

    start_time = time.time()
    chat_id = message.chat.id
    mention = message.from_user.mention

    await message.delete()
    seek_chats.pop(chat_id, None)

    # ───── REPLY AUDIO ─────
    if message.reply_to_message:
        file_path, m = await processReplyToMessage(message)
        if not file_path:
            return await message.reply_text("❌ Reply to an audio / voice note.")

        status, text = await Userbot.playAudio(chat_id, file_path)
        if not status:
            return await m.edit(text)

        audio = message.reply_to_message.audio or message.reply_to_message.voice
        title = message.reply_to_message.text or "Telegram Audio"

        last_played_title[chat_id] = title

        if chat_id in QUEUE:
            q = add_to_queue(chat_id, title, audio.duration, file_path, mention)
            await m.edit(f"**#{q} Added to queue**")
            return asyncio.create_task(delete_messages(message, m))

        await m.edit(
            f"**🎶 Playing in VC**\n\n"
            f"**Title:** {title[:25]}\n"
            f"**Duration:** {audio.duration}\n"
            f"**Requested by:** {mention}"
        )
        return asyncio.create_task(delete_messages(message, m))

    # ───── TEXT QUERY ─────
    if len(message.command) < 2:
        return await message.reply_text("❌ Give song name.")

    m = await message.reply_text("🔍 Searching...")
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

    if chat_id in QUEUE:
        q = add_to_queue(chat_id, title, duration, stream_url, mention)
        await m.edit(f"**#{q} Added to queue**")
        return asyncio.create_task(delete_messages(message, m))

    status, text = await Userbot.playAudio(chat_id, stream_url)
    if not status:
        return await m.edit(text)

    add_to_queue(chat_id, title, duration, stream_url, mention)

    await m.edit(
        f"**🎶 Playing in VC**\n\n"
        f"**Title:** {title[:25]}\n"
        f"**Duration:** {duration}\n"
        f"**Requested by:** {mention}"
    )
    return asyncio.create_task(delete_messages(message, m))


# ─────────────────────────────
# PLAY FORCE (ADMIN ONLY)
# ─────────────────────────────
@app.on_message(
    filters.command(PLAYFORCE_COMMAND, [PREFIX, RPREFIX])
    & filters.group
)
async def playforce(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = message.from_user.mention

    await message.delete()
    seek_chats.pop(chat_id, None)

    if len(message.command) < 2:
        return await message.reply_text("❌ Give song name.")

    admins = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]

    if message.from_user.id not in admins and message.from_user.id not in SUDOERS:
        return await message.reply_text("❌ Only admins can use playforce.")

    m = await message.reply_text("⚡ Force playing...")
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

    status, text = await Userbot.playAudio(chat_id, stream_url)
    if not status:
        return await m.edit(text)

    await m.edit(
        f"**⚡ Force Playing**\n\n"
        f"**Title:** {title[:25]}\n"
        f"**Duration:** {duration}\n"
        f"**Requested by:** {mention}"
    )
    return asyncio.create_task(delete_messages(message, m))

