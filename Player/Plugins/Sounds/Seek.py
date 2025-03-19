from Player import app
from Player.Core import Userbot
from pyrogram import filters
import asyncio
import config
from Player.Utils.Queue import QUEUE

SEEK_COMMAND = ["seek"]
PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


async def trim_audio(input_path, output_path, seek_time):
    """ Trims the audio using ffmpeg from a given seek time. """
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-ss", str(seek_time),
        "-acodec", "copy",
        output_path
    ]
    process = await asyncio.create_subprocess_exec(
        *cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    await process.communicate()
    return output_path


@app.on_message((filters.command(SEEK_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def seek_audio(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = f"[{user_name}](tg://user?id={user_id})"

    if len(message.command) < 2:
        return await message.reply_text("**Usage:** /seek <seconds>")

    try:
        seek_time = int(message.command[1])
        if seek_time < 0:
            return await message.reply_text("❌ **Invalid Seek Time! Use Positive Value.**")

        if chat_id not in QUEUE or not QUEUE[chat_id]:
            return await message.reply_text("❌ **No song is currently playing!**")

        # 🔍 DEBUGGING: Print queue structure
        print(f"Queue Structure for {chat_id}: {QUEUE[chat_id]}")

        # Extract song info - Handling multiple queue formats
        song_info = None
        if isinstance(QUEUE[chat_id], dict):
            song_info = QUEUE[chat_id]  # Direct dictionary case
        elif isinstance(QUEUE[chat_id], list) and isinstance(QUEUE[chat_id][0], dict):
            song_info = QUEUE[chat_id][0]  # First item in queue (list of dicts)

        # Check if song_info is valid
        if not song_info or "file_path" not in song_info:
            return await message.reply_text("❌ **Unable to find the currently playing song file.**")

        song_path = song_info["file_path"]
        new_song_path = f"{song_path}_seeked.mp3"

        await message.reply_text(f"⏩ Seeking to `{seek_time}` seconds...")

        trimmed_song_path = await trim_audio(song_path, new_song_path, seek_time)

        # Stop current playback before playing the new file
        await Userbot.stopAudio(chat_id)  
        Status, Text = await Userbot.playAudio(chat_id, trimmed_song_path)

        if Status == False:
            return await message.reply_text(f"❌ Error: {Text}")

        await message.reply_text(
            f"✅ **Skipped to {seek_time} seconds!**\n🎵 **Now Playing:** {song_info.get('title', 'Unknown')}\n🎤 **Requested by:** {mention}"
        )

    except ValueError:
        return await message.reply_text("❌ **Invalid Seek Time! Enter a number (in seconds).**")
        
