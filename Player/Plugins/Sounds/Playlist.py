"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from Player import app
from Player.Core import Userbot
from Player.Utils.YtDetails import searchPlaylist, extract_playlist_id
from Player.Utils.Queue import QUEUE, add_to_queue, clear_queue
from Player.Plugins.Sounds.Play import ytdl

from pyrogram import filters
import asyncio
import time
import config

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX

PLAYLIST_COMMAND = ["PL", "PLAYLIST"]

@app.on_message((filters.command(PLAYLIST_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id

    if len(message.command) < 2:
        return await message.reply_text("❌ Please enter a playlist name or YouTube playlist link.")

    m = await message.reply_text("🔍 Searching for your playlist...")

    query = message.text.split(maxsplit=1)[1]
    video_id = extract_playlist_id(query)

    if not video_id:  
        # If no playlist ID is found, assume it's a normal search query
        video_id = query  
        await m.edit("🔄 No direct playlist link found. Searching YouTube instead...")

    try:
        title, videoCount, link = searchPlaylist(video_id)

        if not title or not videoCount or not link:
            return await m.edit("❌ No results found. Please check the playlist link or try a different search.")

        videoCount = int(videoCount)
        total_videos = videoCount

    except Exception as e:
        return await m.edit(f"⚠️ Error fetching playlist: <code>{e}</code>")

    await m.edit(f"✅ Playlist Found: **{title}**\n🎵 Fetching songs...")

    # Validate if the link is correct
    if not link.startswith("http"):
        return await m.edit("❌ The extracted playlist link is invalid. Please check and try again.")

    format = "bestaudio"
    try:
        resp, songlinks = await ytdl(format, link)

        if resp == 0 or not songlinks:
            return await m.edit(f"❌ yt-dlp error detected\n\n» `{songlinks}`")

        songlinks = songlinks.strip().split("\n")

        if not songlinks:
            return await m.edit("❌ The playlist is empty or could not be retrieved.")

        songlinkplay = songlinks[0]

        for songlink in songlinks:
            if videoCount == 0:
                break
            add_to_queue(chat_id, title[:19], videoCount, songlink, link)
            videoCount -= 1

        Status, Text = await Userbot.playAudio(chat_id, songlinkplay)

        if not Status:
            return await m.edit(Text)

        finish_time = time.time()
        total_time_taken = str(int(finish_time - start_time)) + "s"

        await m.edit(
            f"🎶 Playing all songs from **[{title[:19]}]({link})**\n"
            f"📌 **Total Videos:** {total_videos}\n"
            f"⏳ **Time Taken:** {total_time_taken}",
            disable_web_page_preview=True,
        )
    
    except Exception as e:
        return await m.edit(f"❌ Error occurred while processing playlist:\n`{str(e)}`")
