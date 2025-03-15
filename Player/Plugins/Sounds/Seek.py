"""
import asyncio
from pyrogram import filters
from Player import app, call
from pytgcalls.types import MediaStream, AudioQuality


playing_tracks = {}

async def play_audio(chat_id, audio_url, seek_time=0):
    """ Plays an audio file from a specific timestamp """
    try:
        if seek_time > 0:
            audio_url += f"#t={seek_time}"  # Append timestamp for seeking

        await call.play(
            chat_id,
            MediaStream(
                audio_url,
                audio_parameters=AudioQuality.STUDIO
            ),
        )

        # ✅ Save the playing song
        playing_tracks[chat_id] = {"url": audio_url, "seek_time": seek_time}
        return True
    except Exception as e:
        return f"❌ Error: `{e}`"


@app.on_message(filters.command("seek"))
async def seek_audio(client, message):
    """ Command: /seek <seconds> - Seek forward or rewind """
    if len(message.command) < 2:
        await message.reply("❌ **Usage:** /seek <seconds>")
        return
    
    chat_id = message.chat.id
    if chat_id not in playing_tracks:
        await message.reply("❌ **No song is currently playing!** Start with `/play <URL>`")
        return

    try:
        seek_time = int(message.command[1])  # Convert seconds to integer
        audio_url = playing_tracks[chat_id]["url"]  # Get current playing URL

        await call.stop(chat_id)  # Stop the current stream
        await play_audio(chat_id, audio_url, seek_time)  # Restart from new position
        await message.reply(f"⏩ **Seeked to:** {seek_time} seconds")
    except Exception as e:
        await message.reply(f"❌ **Error:** `{e}`")
"""

### For Read Only
