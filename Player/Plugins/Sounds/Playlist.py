"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from Player import app
from Player.Core import Userbot
from Player.Utils.YtDetails import extract_playlist_id, get_playlist_videos
from Player.Utils.Queue import QUEUE, add_to_queue, clear_queue
from Player.Utils.YtDetails import ytdl  # ✅ Import ytdl function
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
        return await message.reply_text("❌ Please enter a YouTube playlist link.")

    m = await message.reply_text("🔍 Searching for your playlist...")

    query = message.text.split(maxsplit=1)[1]
    playlist_id = extract_playlist_id(query)

    if not playlist_id:
        return await m.edit("❌ Invalid playlist link. Please provide a valid YouTube playlist URL.")

    try:
        videos = get_playlist_videos(playlist_id)

        if not videos:
            return await m.edit("❌ No videos found in this playlist.")

        total_videos = len(videos)
        await m.edit(f"✅ Playlist Found! **Fetching {total_videos} songs...**")

    except Exception as e:
        return await m.edit(f"⚠️ Error fetching playlist: `{e}`")

    first_song = None

    for index, (title, duration, link) in enumerate(videos, start=1):
        add_to_queue(chat_id, title[:19], duration, link, link)
        if index == 1:
            first_song = link  # ✅ Get first song for playback

    if not first_song:
        return await m.edit("❌ Unable to fetch first song from playlist.")

    # ✅ Get direct audio URL
    status, direct_audio_url, duration = await ytdl("bestaudio", first_song)  # Fixed

    # ✅ Check for errors
    if status == 0 or not direct_audio_url:
        return await m.edit(f"❌ yt-dlp Error: {direct_audio_url}")

    # ✅ Play the first song in VC
    Status, Text = await Userbot.playAudio(chat_id, direct_audio_url)
    if not Status:
        return await m.edit(Text)

    finish_time = time.time()
    total_time_taken = str(int(finish_time - start_time)) + "s"

    await m.edit(
        f"🎶 Now Playing from **Playlist**\n"
        f"📌 **Total Videos:** {total_videos}\n"
        f"⏳ **Time Taken:** {total_time_taken}",
        disable_web_page_preview=True,
    )
