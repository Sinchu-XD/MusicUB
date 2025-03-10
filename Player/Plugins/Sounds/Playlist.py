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
import random
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
        await message.reply_text("PLease enter song name or yt link")
    else:
        m = await message.reply_text("Searching for your song")
        query = message.text.split(maxsplit=1)[1]
        video_id = extract_playlist_id(query)
        try:
            if video_id is None:
                video_id = query
            title, videoCount, link = searchPlaylist(video_id)
            if (title, videoCount, link) == (None, None, None):
                return await m.edit("No results found")
            videoCount = int(videoCount)
            total_videos = videoCount
        except Exception as e:
            await message.reply_text(f"Error:- <code>{e}</code>")
            return

        await m.edit("Found the match... Downloading your song...")
        format = "bestaudio"
        resp, songlinks = await ytdl(format, link)
        if resp == 0:
            await m.edit(f"❌ yt-dl issues detected\n\n» `{songlink}`")
        else:
            songlinks = songlinks.split("\n")
            # just get the first line from songlinks
            songlinkplay = songlinks[0]
            for songlink in songlinks:
                if videoCount == 0:
                    break
                elif videoCount is None:
                    await m.edit("The Playlist is empty!")
                    break
                add_to_queue(chat_id, title[:19], videoCount, songlink, link)
                videoCount -= 1

            Status, Text = await Userbot.playAudio(chat_id, songlinkplay)
            if Status == False:
                return await m.edit(Text)
            finish_time = time.time()
            total_time_taken = str(int(finish_time - start_time)) + "s"
            await m.edit(
                f"Playing all songs from\nPlaylist Name:- [{title[:19]}]({link})\nTotal Videos:- {total_videos}\nTime taken to play:- {total_time_taken}",
                disable_web_page_preview=True,
            )
