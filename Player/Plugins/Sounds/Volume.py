"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import asyncio
import config

from pyrogram import filters
from pytgcalls.types import MediaStream, AudioQuality

from Player import app, call
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

    chat_queue = get_queue(chat_id)
    songlink = chat_queue[0][2]

    try:
        volume = int(message.text.split()[1])

        if volume < 1 or volume > 200:
            return await message.reply_text("⚠️ Volume must be between 1 and 200.")

        volume_levels[chat_id] = volume

        await call.play(
            chat_id,
            MediaStream(
                media_path=songlink,
                audio_parameters=AudioQuality.HIGH,
                ffmpeg_parameters=f"-filter:a volume={volume / 100}"
            )
        )

        m = await message.reply_text(f"🔊 Volume set to **{volume}%**.")
        return asyncio.create_task(delete_messages(message, m))

    except IndexError:
        current = volume_levels.get(chat_id, 100)
        m = await message.reply_text(f"🔈 Current volume is **{current}%**.")
        return asyncio.create_task(delete_messages(message, m))

    except ValueError:
        m = await message.reply_text("❌ Invalid volume value.\nUse `/volume 80` (1-200)")
        return asyncio.create_task(delete_messages(message, m))

    except Exception as e:
        m = await message.reply_text(f"❌ Error:\n`{e}`")
        return asyncio.create_task(delete_messages(message, m))
