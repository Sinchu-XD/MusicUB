"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from Player import app, call
from Player.Core import Userbot
from Player.Utils.YtDetails import searchYt, extract_video_id
from Player.Utils.Queue import QUEUE, add_to_queue, get_queue, remove_first_from_queue
from Player.Utils.Delete import delete_messages
from pyrogram import filters
import asyncio
import time
import config
import yt_dlp

PLAY_COMMAND = ["PLY"]
PLAYFORCE_COMMAND = ["PLFORCE"]

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
            return info.get("url", None)
    except Exception:
        return None


async def process_audio_reply(message):
    msg = message.reply_to_message
    if msg and (msg.audio or msg.voice):
        return await msg.download()
    return None


async def play_next_song(chat_id):
    """Plays the next song in the queue automatically."""
    if chat_id not in QUEUE or not get_queue(chat_id):
        return await call.leave_group_call(chat_id)

    song = remove_first_from_queue(chat_id)
    title, duration, songlink, link = song

    status, text = await Userbot.playAudio(chat_id, songlink)
    if not status:
        return await app.send_message(chat_id, f"❌ **Error playing next song:** `{text}`")

    await app.send_message(
        chat_id,
        f"🎶 **Now Playing**\n**{title[:19]}**\n**Duration:** {duration}",
        disable_web_page_preview=True,
    )


@app.on_message(filters.command(PLAY_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def _aPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    # Handle Reply to Audio
    if message.reply_to_message:
        input_filename = await process_audio_reply(message)
        if not input_filename:
            return await message.reply_text("❌ **Provide a song link or reply to a voice note.**")

        if chat_id in QUEUE and get_queue(chat_id):
            add_to_queue(chat_id, "Audio File", "Unknown", input_filename, None)
            return await message.reply_text(f"🎵 **Added Audio to Queue.**")

        status, text = await Userbot.playAudio(chat_id, input_filename)
        if not status:
            return await message.reply_text(text)

        return await message.reply_text(
            f"🎵 **Now Playing in VC**\n**Requested By**: {mention}\n"
            f"**Response Time**: {int(time.time() - start_time)}s",
            disable_web_page_preview=True,
        )

    # If No Song Name Provided
    if len(message.command) < 2:
        return await message.reply_text("❌ **Provide a song link or name.**")

    m = await message.reply_text("🔍 **Searching...**")
    query = message.text.split(maxsplit=1)[1]
    video_id = extract_video_id(query) or query

    try:
        title, duration, link = searchYt(video_id)
        if not title:
            return await m.edit("❌ **No results found.**")
    except Exception as e:
        return await m.edit(f"⚠ **Error:** `{e}`")

    songlink = await ytdl(link)
    if not songlink:
        return await m.edit("❌ **Failed to fetch song.**")

    # If Song is Already Playing, Add to Queue Instead
    if chat_id in QUEUE:
        queue_num = add_to_queue(chat_id, title[:19], duration, songlink, link)
        await m.edit(
                    f"# {queue_num}\n{title[:19]}\n**ʏᴏᴜʀ ꜱᴏɴɢ ᴀᴅᴅᴇᴅ ɪɴ Qᴜᴇᴜᴇ\n\nᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ 😵‍💫**"
                )
                
        return

    # Play the Song
    status, text = await Userbot.playAudio(chat_id, songlink)
    if not status:
        return await m.edit(text)

    await m.edit(
        f"🎶 **Now Playing in VC**\n**Song**: [{title[:19]}]({link})\n"
        f"**Duration**: {duration}\n**Requested By**: {mention}\n"
        f"**Response Time**: {int(time.time() - start_time)}s",
        disable_web_page_preview=True,
    )


@app.on_message(filters.command(PLAYFORCE_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def playforce(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = f"[{message.from_user.first_name}](tg://user?id={message.from_user.id})"

    if len(message.command) < 2:
        return await message.reply_text("❌ **Provide a song link or name.**")

    m = await message.reply_text("🔍 **Searching...**")
    query = message.text.split(maxsplit=1)[1]
    video_id = extract_video_id(query) or query

    try:
        title, duration, link = searchYt(video_id)
        if not title:
            return await m.edit("❌ **No results found.**")
    except Exception as e:
        return await m.edit(f"⚠ **Error:** `{e}`")

    songlink = await ytdl(link)
    if not songlink:
        return await m.edit("❌ **Failed to fetch song.**")

    # Clear Queue and Force Play
    QUEUE[chat_id] = []  # Clears the queue
    status, text = await Userbot.playAudio(chat_id, songlink)
    if not status:
        return await m.edit(text)

    await m.edit(
        f"🎶 **Now Playing (Forced) in VC**\n**Song**: [{title[:19]}]({link})\n"
        f"**Duration**: {duration}\n**Requested By**: {mention}\n"
        f"**Response Time**: {int(time.time() - start_time)}s",
        disable_web_page_preview=True,
    )


@call.on_stream_end(())
async def _on_stream_end(_, chat_id):
    """Automatically plays the next song when the current one ends."""
    await play_next_song(chat_id)
