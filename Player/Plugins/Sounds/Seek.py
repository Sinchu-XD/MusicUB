"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from Player import app, call
from Player.Utils.Loop import get_loop
from Player.Utils.Delete import delete_messages
from Player.Utils.Queue import QUEUE, get_queue

from pyrogram import filters
from pytgcalls.types import MediaStream, AudioQuality

seek_chats = {}

@app.on_message((filters.command("seek", [PREFIX, RPREFIX])) & filters.group)
async def seek_audio(_, message):
    chat_id = message.chat.id
    if chat_id not in QUEUE:
        return await message.reply_text("No song playing...")
    try:
        seek_dur = int(message.text.split()[1])
    except:
        return await message.reply_text("Usage: /seek time (int)\n\nExample: `/seek 10`")

    chat_queue = get_queue(chat_id)
    songlink = chat_queue[0][3]
    try:
        seeked_dur = seek_chats.get(chat_id, 0)
        duration = await call.time(chat_id)
        duration += seek_dur + seeked_dur
        await call.play(
            chat_id,
            MediaStream(
                media_path=songlink,
                audio_parameters=AudioQuality.HIGH,
                video_flags=MediaStream.Flags.IGNORE,
                ffmpeg_parameters="-ss {0}".format(duration),
            ),
        )
        seek_chats[chat_id] = duration
        return await message.reply_text("Seeked {} seconds".format(seek_dur))
    except Exception as e:
        return await message.reply_text(f"Error: <code>{e}</code>")
