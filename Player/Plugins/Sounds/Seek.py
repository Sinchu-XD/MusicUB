import asyncio
from pyrogram import filters
from Player import app, call
from pytgcalls.types import MediaStream, AudioQuality


async def play_audio(chat_id, audio_url, seek_time=0):
    """ Function to play audio from a specific timestamp """
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
        playing_tracks[chat_id] = audio_url  # Store the track being played
        return True
    except Exception as e:
        return f"❌ Error: `{e}`"


@app.on_message(filters.command("seek"))
async def seek_audio(client, message):
    """ Command to seek audio """
    chat_id = message.chat.id
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /seek <seconds>")
        return
    
    if chat_id not in playing_tracks:
        await message.reply_text("❌ **No song is currently playing!**")
        return

    try:
        seek_time = int(message.command[1])  # Convert seconds to integer
        audio_url = playing_tracks[chat_id]  # Get current playing URL

        await call.stop(chat_id)  # Stop the current stream
        await play_audio(chat_id, audio_url, seek_time)  # Replay from new position
        await message.reply_text(f"⏩ **Seeked to:** {seek_time} seconds")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{e}`")
