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
        return await message.reply_text("❌ Nothing is playing currently.")

    try:
        vol_input = int(message.text.split()[1])
        if vol_input < 0 or vol_input > 200:
            raise ValueError
    except (IndexError, ValueError):
        msg = await message.reply_text("Usage: /volume [0-200]\nExample: `/volume 100`")
        return await delete_messages(message, msg)

    try:
        queue = get_queue(chat_id)
        songlink = queue[0][2]
        seek = seek_chats.get(chat_id, 0)
        ffmpeg_volume = vol_input / 100

        await call.play(
            chat_id,
            MediaStream(
                media_path=songlink,
                audio_parameters=AudioQuality.HIGH,
                ffmpeg_parameters=f"-ss {seek} -filter:a volume={ffmpeg_volume}"
            ),
        )

        msg = await message.reply_text(f"🔊 Volume set to `{vol_input}%`.")
        await delete_messages(message, msg)

    except Exception as e:
        msg = await message.reply_text(f"❌ Failed to set volume:\n`{e}`")
        await delete_messages(message, msg)
