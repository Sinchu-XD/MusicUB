"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""
from Player import app, call
from Player.Core import Userbot
from Player.Utils.YtDetails import searchYt, extract_video_id
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Utils.Delete import delete_messages
from Player.Misc import SUDOERS

from pyrogram import filters
import asyncio
import time
import config
import yt_dlp

PLAY_COMMAND = ["PLAYS", "PLY"]
PLAYFORCE_COMMAND = ["PFRCE", "PLAYFORC"]

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


async def ytdl(link: str):
    ydl_opts = {
        "format": "bestaudio",
        "geo_bypass": True,
        "noplaylist": True,
        "quiet": True,
        "cookiefile": "cookies/cookies.txt",
        "nocheckcertificate": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return (1, info["url"]) if "url" in info else (0, "No URL found")
    except Exception as e:
        return (0, str(e))


async def process_audio_reply(message):
    msg = message.reply_to_message
    if msg and (msg.audio or msg.voice):
        m = await message.reply_text("🎶 **Downloading Your Song...**")
        input_filename = await msg.download()
        return input_filename, m
    return None, None


@app.on_message(filters.command(PLAY_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def _aPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    # Process if replying to an audio/voice
    if message.reply_to_message:
        input_filename, m = await process_audio_reply(message)
        if not input_filename:
            return await message.reply_text("❌ **Provide a song link or reply to a voice note.**")

        await m.edit("⏳ **Processing...**")
        status, text = await Userbot.playAudio(chat_id, input_filename)
        if not status:
            return await m.edit(text)

        finish_time = time.time()
        total_time_taken = f"{int(finish_time - start_time)}s"

        await m.edit(
            f"🎵 **Now Playing in VC**\n\n"
            f"**Requested By**: {mention}\n"
            f"**Response Time**: {total_time_taken}",
            disable_web_page_preview=True,
        )
        asyncio.create_task(delete_messages(message, m))
        return

    # If user provides a song name/link
    if len(message.command) < 2:
        return await message.reply_text("❌ **Provide a song link or name.**")

    m = await message.reply_text("🔍 **Searching for your song...**")
    query = message.text.split(maxsplit=1)[1]
    video_id = extract_video_id(query) or query

    try:
        title, duration, link = searchYt(video_id)
        if not title:
            return await m.edit("❌ **No results found.**")
    except Exception as e:
        return await m.edit(f"⚠ **Error:** `{e}`")

    await m.edit("⏳ **Fetching song details...**")
    resp, songlink = await ytdl(link)

    if resp == 0:
        return await m.edit(f"❌ **Error with yt-dlp:** `{songlink}`")

    # Queue handling
    if chat_id in QUEUE:
        queue_num = add_to_queue(chat_id, title[:19], duration, songlink, link)
        return await m.edit(
            f"🎵 **#{queue_num} {title[:19]}**\n"
            f"**Song added to queue. Please wait.**"
        )

    # Play song instantly
    status, text = await Userbot.playAudio(chat_id, songlink)
    if not status:
        return await m.edit(text)

    finish_time = time.time()
    total_time_taken = f"{int(finish_time - start_time)}s"

    await m.edit(
        f"🎶 **Now Playing in VC**\n\n"
        f"**Song**: [{title[:19]}]({link})\n"
        f"**Duration**: {duration}\n"
        f"**Requested By**: {mention}\n"
        f"**Response Time**: {total_time_taken}",
        disable_web_page_preview=True,
    )

    asyncio.create_task(delete_messages(message, m))


@app.on_message(filters.command(PLAYFORCE_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def playforce(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    if len(message.command) < 2:
        return await message.reply_text("❌ **Provide a song link or name.**")

    m = await message.reply_text("🔍 **Searching for your song...**")
    query = message.text.split(maxsplit=1)[1]
    video_id = extract_video_id(query) or query

    try:
        title, duration, link = searchYt(video_id)
        if not title:
            return await m.edit("❌ **No results found.**")
    except Exception as e:
        return await m.edit(f"⚠ **Error:** `{e}`")

    await m.edit("⏳ **Fetching song details...**")
    resp, songlink = await ytdl(link)

    if resp == 0:
        return await m.edit(f"❌ **Error with yt-dlp:** `{songlink}`")

    # Force play the song
    status, text = await Userbot.playAudio(chat_id, songlink)
    if not status:
        return await m.edit(text)

    finish_time = time.time()
    total_time_taken = f"{int(finish_time - start_time)}s"

    await m.edit(
        f"🎶 **Now Playing (Forced) in VC**\n\n"
        f"**Song**: [{title[:19]}]({link})\n"
        f"**Duration**: {duration}\n"
        f"**Requested By**: {mention}\n"
        f"**Response Time**: {total_time_taken}",
        disable_web_page_preview=True,
    )

    asyncio.create_task(delete_messages(message, m))
  
