"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import asyncio
import config

from pyrogram import filters
from pytgcalls.types import MediaStream, AudioQuality

from Player import app, call, seek_chats
from Player.Utils.Loop import get_loop
from Player.Utils.Delete import delete_messages
from Player.Utils.Queue import get_queue

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


@app.on_message(filters.command("seek", [PREFIX, RPREFIX]) & filters.group)
async def seek_audio(_, message):
    chat_id = message.chat.id

    # ───── CHECK QUEUE ─────
    queue = get_queue(chat_id)
    if not queue:
        return await message.reply_text("❌ **No song is currently playing.**")

    # ───── PARSE SEEK VALUE ─────
    try:
        seek_dur = int(message.text.split()[1])
    except (IndexError, ValueError):
        m = await message.reply_text(
            "**Usage:** `/seek <seconds>`\n\n"
            "➤ Forward: `/seek 10`\n"
            "➤ Rewind: `/seek -10`"
        )
        return asyncio.create_task(delete_messages(message, m))

    # ───── LOOP SAFETY ─────
    if await get_loop(chat_id) > 0:
        m = await message.reply_text(
            "🔄 **Loop is enabled.**\n"
            "Disable loop before using seek."
        )
        return asyncio.create_task(delete_messages(message, m))

    # ───── CURRENT SONG ─────
    title, duration, stream_url, requested_by = queue[0]

    current_seek = seek_chats.get(chat_id, 0)
    new_seek = current_seek + seek_dur
    if new_seek < 0:
        new_seek = 0

    # ───── APPLY SEEK ─────
    try:
        await call.play(
            chat_id,
            MediaStream(
                media_path=stream_url,
                audio_parameters=AudioQuality.HIGH,
                ffmpeg_parameters=f"-ss {new_seek}",
            ),
        )

        seek_chats[chat_id] = new_seek

        direction = "forward" if seek_dur >= 0 else "rewind"
        m = await message.reply_text(
            f"✅ **Seeked {abs(seek_dur)}s {direction}.**\n"
            f"🎧 **Now at:** `{new_seek}` seconds"
        )
        return asyncio.create_task(delete_messages(message, m))

    except Exception as e:
        m = await message.reply_text(f"❌ **Seek failed:**\n`{e}`")
        return asyncio.create_task(delete_messages(message, m))
