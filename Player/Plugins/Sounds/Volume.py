"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import asyncio
import config

from pyrogram import filters
from pytgcalls.types import MediaStream, AudioQuality

from Player import app, call, seek_chats
from Player.Utils.Queue import QUEUE, get_queue
from Player.Utils.Delete import delete_messages

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX

volume_levels = {}

@app.on_message(filters.command("volume", [PREFIX, RPREFIX]) & filters.group)
async def set_volume(_, message):
    chat_id = message.chat.id

    if chat_id not in QUEUE:
        return await message.reply_text("❌ No song is currently playing.")

    try:
        volume = int(message.text.split()[1])
    except (IndexError, ValueError):
        current = volume_levels.get(chat_id, 100)
        msg = await message.reply_text(f"🔈 Current volume is **{current}%**.\nUse `/volume 1-200`")
        return asyncio.create_task(delete_messages(message, msg))

    if not 1 <= volume <= 200:
        msg = await message.reply_text("⚠️ Volume must be between 1 and 200.")
        return asyncio.create_task(delete_messages(message, msg))

    chat_queue = get_queue(chat_id)
    songlink = chat_queue[0][2]
    seek_dur = seek_chats.get(chat_id, 0)

    try:
        await call.play(
            chat_id,
            MediaStream(
                media_path=songlink,
                audio_parameters=AudioQuality.HIGH,
                ffmpeg_parameters=f"-ss {seek_dur} -filter:a volume={volume / 100}"
            )
        )

        volume_levels[chat_id] = volume
        seek_chats[chat_id] = seek_dur

        msg = await message.reply_text(f"🔊 Volume set to **{volume}%**.")
        return asyncio.create_task(delete_messages(message, msg))

    except Exception as e:
        msg = await message.reply_text(f"❌ Failed to change volume:\n`{e}`")
        return asyncio.create_task(delete_messages(message, msg))
