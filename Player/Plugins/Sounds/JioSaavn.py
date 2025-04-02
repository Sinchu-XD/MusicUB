from pyrogram import filters
from Player import app
from Player.Utils.JioSaavn import get_song
from Player.Core.Userbot import playAudio

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX
PLAY_COMMAND = ["JPLAY", "JIOSAAVN"]


@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def jio_play(_, message):
    """Play a JioSaavn song in VC."""
    if len(message.command) < 2:
        return await message.reply_text("Usage: /jplay [song name]")

    query = message.text.split(None, 1)[1]
    song = get_song(query)

    if not song:
        return await message.reply_text("No song found!")

    await message.reply_photo(
        photo=song["thumbnail"],
        caption=f"🎵 **{song['title']}**\n👤 {song['artist']}\n🔗 [Listen on JioSaavn]({song['url']})"
    )

    response = await playAudio(message.chat.id, song["media_url"])
    await message.reply_text(response)
  
