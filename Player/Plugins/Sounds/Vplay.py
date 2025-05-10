"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from Player import app, call, seek_chats
from Player.Core import Userbot
import yt_dlp
from YouTubeMusic.Search import Search
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Utils.Delete import delete_messages
from Player.Misc import SUDOERS
from pyrogram import filters
import os
import re
import glob
import asyncio
import time
import config

PLAY_COMMAND = ["V", "VPLAY"]
PLAYFORCE_COMMAND = ["VPFORCE", "VPLAYFORCE"]
PREFIX = config.PREFIX
RPREFIX = config.RPREFIX

async def SearchYt(query: str):
    results = Search(query, limit=1)

    if not results:
        raise Exception("No results found.")

    search_data = []
    for item in results:
        search_data.append({
            "title": item["title"],
            "artist": item["artist_name"],
            "channel": item["channel_name"],
            "duration": item["duration"],
            "views": item["views"],
            "thumbnail": item["thumbnail"],
            "url": item["url"]
        })

    stream_url = results[0]["url"]
    
    return search_data, stream_url

async def ytdl(format: str, url: str):

    ydl_opts = {
        'format': format,
        'geo_bypass': True,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': COOKIES_FILE,
        'nocheckcertificate': True,
        'force_generic_extractor': True,
        'extractor_retries': 3,
        'outtmpl': cached_path,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            logging.info(f"Downloaded file: {cached_path}")
            return (1, cached_path)
    except Exception as e:
        logging.error(f"Error during download: {e}")
        return (0, str(e))


def clean_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '', name).strip().replace(' ', '_')

async def processReplyToMessage(message):
    msg = message.reply_to_message
    if msg and (msg.video or msg.video_note):
        m = await message.reply_text("Rukja... Tera video download kar raha hu...")

        file_name = getattr(msg.video, "file_name", None) or "video.mp4"
        safe_file_name = clean_filename(file_name)
        try:
            video_original = await msg.download(file_name=f"downloads/{safe_file_name}")
            return video_original, m
        except Exception as e:
            await m.edit(f"❌ Download failed: `{e}`")
            return None, m
    return None, None

@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = message.from_user.mention

    if chat_id in seek_chats:
        seek_chats.pop(chat_id)

    if message.reply_to_message and (message.reply_to_message.video or message.reply_to_message.video_note):
        input_filename, m = await processReplyToMessage(message)
        if not input_filename:
            return

        await m.edit("Rukja...Tera Video Play kar raha hu...")
        Status, Text = await Userbot.playVideo(chat_id, input_filename)
        if not Status:
            return await m.edit(Text)

        video = message.reply_to_message.video or message.reply_to_message.video_note
        video_title = message.reply_to_message.text or "Unknown"
        await message.delete()

        if chat_id in QUEUE:
            queue_num = add_to_queue(
                chat_id,
                video_title[:19],
                video.duration,
                video.file_id,
                message.reply_to_message.link,
            )
            await m.edit(f"# {queue_num}\n{video_title[:19]}\nTera video queue me daal diya hu")
        else:
            finish_time = time.time()
            total_time_taken = str(int(finish_time - start_time)) + "s"
            await m.edit(
                f"Tera video play kar rha hu aaja vc\n\n"
                f"VideoName:- [{video_title[:19]}]({message.reply_to_message.link})\n"
                f"Duration:- {video.duration}\n"
                f"Time taken to play:- {total_time_taken}",
                disable_web_page_preview=True,
            )
        return asyncio.create_task(delete_messages(message, m))

    # Check if query was provided
    if len(message.text.split(maxsplit=1)) < 2:
        return await message.reply_text("❌ Please provide a video name or URL.\n\n**Usage:** `/vplay <video name or link>`")

    query = message.text.split(maxsplit=1)[1]
    m = await message.reply_text("**ᴡᴀɪᴛ ɴᴀ ʏʀʀʀ\n\nꜱᴇᴀʀᴄʜɪɴɢ ʏᴏᴜʀ ꜱᴏɴɢ 🌚❤️..**")

    try:
        search_results, stream_url = await SearchYt(query)
        if not search_results:
            return await m.edit("No results found.")
    except Exception as e:
        return await m.edit(f"Error: <code>{e}</code>")

    status, songlink = await ytdl("best[height<=?720][width<=?1280]", stream_url)
    if not status or not songlink:
        return await m.edit(f"❌ yt-dl issues detected\n\n» No valid song link found.")

    title = search_results[0]['title']
    duration = search_results[0]['duration']
    channel = search_results[0]['channel']
    views = search_results[0]['views']
    total_time = f"{int(time.time() - start_time)} **Seconds**"

    if chat_id in QUEUE:
        queue_num = add_to_queue(chat_id, search_results, songlink, stream_url)
        await m.edit(
            f"# **{queue_num} ʏᴏᴜʀ ꜱᴏɴɢ ᴀᴅᴅᴇᴅ ɪɴ Qᴜᴇᴜᴇ**\n\n"
            f"**SongName :** [{title[:19]}]({stream_url})\n"
            f"**Duration :** {duration} **Minutes**\n"
            f"**Channel :** {channel}\n"
            f"**Views :** {views}\n"
            f"**Requested By :** {mention}\n\n"
            f"**Response Time :** {total_time}",
            disable_web_page_preview=True,
        )
        return asyncio.create_task(delete_messages(message, m))

    Status, Text = await Userbot.playVideo(chat_id, songlink)
    if not Status:
        return await m.edit(Text)

    add_to_queue(chat_id, search_results, songlink, stream_url)
    await m.edit(
        f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n"
        f"**SongName :** [{title[:19]}]({stream_url})\n"
        f"**Duration :** {duration} **Minutes**\n"
        f"**Channel :** {channel}\n"
        f"**Views :** {views}\n"
        f"**Requested By :** {mention}\n\n"
        f"**Response Time :** {total_time}",
        disable_web_page_preview=True,
    )
    return asyncio.create_task(delete_messages(message, m))


@app.on_message((filters.command(PLAYFORCE_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def playforce(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = message.from_user.mention

    seek_chats.pop(chat_id, None)

    if len(message.text.split(maxsplit=1)) < 2:
        return await message.reply_text("**𝑊𝑎𝑖𝑡 𝙶𝚒𝚟𝚎 𝙼𝚎 𝚂𝚘𝚗𝚐 𝙻𝚒𝚗𝚔 𝙾𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚅𝚘𝚒𝚌𝚎 𝙽𝚘𝚝𝚎**")

    query = message.text.split(maxsplit=1)[1]
    m = await message.reply_text("**Force Playing Your Song...**")

    try:
        search_results, stream_url = await SearchYt(query)
        if not search_results:
            return await m.edit("No results found.")
    except Exception as e:
        return await m.edit(f"Error while searching: <code>{e}</code>")

    await m.edit("**Fetching Song Details...**")

    try:
        status, songlink = await ytdl("best[height<=?720][width<=?1280]", stream_url)
        duration = search_results[0]['duration']
    except Exception as e:
        return await m.edit(f"Error while downloading: <code>{e}</code>")

    if not status or not songlink:
        return await m.edit("❌ yt-dl issues detected.\n\n» No valid song link found.")

    QUEUE[chat_id] = [(search_results[0]['title'], message.from_user.id, songlink)]
    seek_chats.pop(chat_id, None)

    Status, Text = await Userbot.playVideo(chat_id, songlink)
    if not Status:
        return await m.edit(Text)

    total_time = f"{int(time.time() - start_time)} **Seconds**"
    await m.edit(
        f"**𝑆𝑜𝑛𝑔 𝐹𝑜𝑟𝑐𝑒 𝑃𝑙𝑎𝑦𝑒𝑑 𝑎𝑡 ν𝑐**\n\n"
        f"**SongName :** [{search_results[0]['title'][:19]}]({stream_url})\n"
        f"**Duration :** {duration} **Minutes**\n"
        f"**Channel :** {search_results[0]['channel']}\n"
        f"**Views :** {search_results[0]['views']}\n"
        f"**Requested By :** {mention}\n\n"
        f"**Response Time :** {total_time}",
        disable_web_page_preview=True,
    )
    return asyncio.create_task(delete_messages(message, m))
    
