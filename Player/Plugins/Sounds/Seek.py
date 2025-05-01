"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import asyncio
import config

from Player import app, call, seek_chats
from Player.Utils.Loop import get_loop
from Player.Utils.Delete import delete_messages
from Player.Utils.Queue import QUEUE, get_queue

from pyrogram import filters
from pytgcalls.types import MediaStream, AudioQuality

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX

@app.on_message((filters.command("seek", [PREFIX, RPREFIX])) & filters.group)
async def seek_audio(_, message):
    chat_id = message.chat.id

    if chat_id not in QUEUE:
        return await message.reply_text("❌ No song is currently playing.")

    try:
        seek_dur = int(message.text.split()[1])
    except (IndexError, ValueError):
        m = await message.reply_text(
            "**Usage:** `/seek <seconds>`\n"
            "➤ Use positive to seek forward (e.g., `/seek 10`)\n"
            "➤ Use negative to rewind (e.g., `/seek -10`)"
        )
        return asyncio.create_task(delete_messages(message, m))

    chat_queue = get_queue(chat_id)
    songlink = chat_queue[0][2]

    current_seek = seek_chats.get(chat_id, 0)
    new_seek = current_seek + seek_dur

    # Prevent seeking to negative time
    if new_seek < 0:
        new_seek = 0

    try:
        await call.play(
            chat_id,
            MediaStream(
                media_path=songlink,
                audio_parameters=AudioQuality.HIGH,
                ffmpeg_parameters=f"-ss {new_seek}",
            ),
        )

        seek_chats[chat_id] = new_seek

        direction = "forward" if seek_dur >= 0 else "rewind"
        m = await message.reply_text(f"✅ Seeked **{abs(seek_dur)}s {direction}**. Now at `{new_seek}` seconds.")
        asyncio.create_task(delete_messages(message, m))

    except Exception as e:
        m = await message.reply_text(f"❌ Error while seeking:\n`{e}`")
        asyncio.create_task(delete_messages(message, m))
