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
from Player.Plugins.Start.Spam import spam_check
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Utils.Delete import delete_messages
from Player.Misc import SUDOERS

# 🔑 Autoplay ke liye last played title
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
# PLAY COMMAND
# ─────────────────────────────
@app.on_message(
    (filters.command(PLAY_COMMAND, [PREFIX, RPREFIX]))
    & filters.group
    & spam_check()
)
async def play_music(_, message):
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

        # 🔑 store last played title (for autoplay)
        last_played_title[chat_id] = title

        if chat_id in QUEUE:
            q = add_to_queue(chat_id, title, audio.duration, file_path, mention)
            await m.edit(f"**#{q} Added to queue**")
            return asyncio.create_task(delete_messages(message, m))

        total_time = int(time.time() - start_time)
        await m.edit(
            f"**🎶 Playing in VC**\n\n"
            f"**Title:** {title[:25]}\n"
            f"**Duration:** {audio.duration}\n"
            f"**Requested by:** {mention}\n"
            f"**Response:** {total_time}s"
        )
        return asyncio.create_task(delete_messages(message, m))

    # ───── TEXT QUERY ─────
    if len(message.command) < 2:
        return await message.reply_text("❌ Give song name or link.")

    m = await message.reply_text("🔍 Searching your song...")
    query = message.text.split(maxsplit=1)[1]

    search_results, stream_url = await SearchYt(query)
    if not search_results:
        return await m.edit("❌ No results found.")

    status, songlink = await Ytdl(stream_url)
    if not status:
        return await m.edit(songlink)

    title = search_results[0]["title"]
    duration = search_results[0]["duration"]

    # 🔑 store last played title (for autoplay)
    last_played_title[chat_id] = title

    total_time = int(time.time() - start_time)

    # ───── QUEUE MODE ─────
    if chat_id in QUEUE:
        q = add_to_queue(chat_id, title, duration, songlink, mention)
        await m.edit(
            f"**#{q} Added to queue**\n\n"
            f"**Title:** {title[:25]}\n"
            f"**Duration:** {duration}\n"
            f"**Requested by:** {mention}"
        )
        return asyncio.create_task(delete_messages(message, m))

    # ───── PLAY NOW ─────
    status, text = await Userbot.playAudio(chat_id, songlink)
    if not status:
        return await m.edit(text)

    add_to_queue(chat_id, title, duration, songlink, mention)

    await m.edit(
        f"**🎶 Playing in VC**\n\n"
        f"**Title:** {title[:25]}\n"
        f"**Duration:** {duration}\n"
        f"**Requested by:** {mention}\n"
        f"**Response:** {total_time}s"
    )
    return asyncio.create_task(delete_messages(message, m))


# ─────────────────────────────
# PLAY FORCE
# ─────────────────────────────
@app.on_message(
    (filters.command(PLAYFORCE_COMMAND, [PREFIX, RPREFIX]))
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
        return await message.reply_text("❌ Only admins / sudo users.")

    m = await message.reply_text("⚡ Force playing...")
    query = message.text.split(maxsplit=1)[1]

    search_results, stream_url = await SearchYt(query)
    if not search_results:
        return await m.edit("❌ No results found.")

    status, songlink = await Ytdl(stream_url)
    if not status:
        return await m.edit(songlink)

    title = search_results[0]["title"]
    duration = search_results[0]["duration"]

    # 🔑 store last played title (for autoplay)
    last_played_title[chat_id] = title

    QUEUE[chat_id] = [(title, duration, songlink, mention)]

    status, text = await Userbot.playAudio(chat_id, songlink)
    if not status:
        return await m.edit(text)

    total_time = int(time.time() - start_time)
    await m.edit(
        f"**⚡ Force Played**\n\n"
        f"**Title:** {title[:25]}\n"
        f"**Duration:** {duration}\n"
        f"**Requested by:** {mention}\n"
        f"**Response:** {total_time}s"
    )
    return asyncio.create_task(delete_messages(message, m))

