from pyrogram import filters
from Player import app
from Player.Utils.JioSaavn import fetch_song_url, extract_mp3
from Player.Core.Userbot import playAudio
import config


PREFIX = config.PREFIX
RPREFIX = config.RPREFIX
PLAY_COMMAND = ["JPLAY", "JIOSAAVN"]


@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def jiosaavn_command(_, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: !jiosaavn <song name>")

    song_name = " ".join(message.command[1:])
    chat_id = message.chat.id

    msg = await message.reply_text("🔍 Searching for song on JioSaavn...")
    
    song_link = fetch_song_url(song_name)
    if not song_link:
        return await msg.edit("⚠ No Song Found.")

    song = extract_mp3(song_link)
    if not song or not song["media_url"]:
        return await msg.edit("⚠ Could not fetch MP3 URL.")

    result = await playAudio(chat_id, song["media_url"])
    await msg.edit(result)
