import logging
from Player import app, call, seek_chats
from Player.Core import Userbot
import yt_dlp
from pyrogram.enums import ChatAction
from pyrogram.types import Message
from Player.Utils.YtDetails import SearchYt
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Utils.Delete import delete_messages
from Player.Misc import SUDOERS
from pyrogram import filters
import os
import re
import asyncio
import time
import config

PLAY_COMMAND = ["V", "VPLAY"]
PLAYFORCE_COMMAND = ["VPFORCE", "VPLAYFORCE"]
PREFIX = config.PREFIX
RPREFIX = config.RPREFIX
COOKIES_FILE = "cookies/cookies.txt"

# Configure logging for better debugging
logging.basicConfig(level=logging.INFO)


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
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            if 'url' in info:
                return (1, info['url'])
            else:
                return (0, "No URL found")
    except Exception as e:
        logging.error(f"Error during download: {e}")
        return (0, str(e))


def clean_filename(name: str) -> str:
    return re.sub(r'[<>:"/\\|?*]', '', name).strip().replace(' ', '_')


last_update = {}

def progress_bar(current, total, message: Message, start_time):
    now = time.time()
    msg_id = message.chat.id

    # Throttle updates to once every 3 seconds or 5% change
    if msg_id in last_update:
        last_time, last_percent = last_update[msg_id]
        percent = int((current / total) * 100)
        if now - last_time < 3 and abs(percent - last_percent) < 5:
            return  # Skip update

    last_update[msg_id] = (now, int((current / total) * 100))

    done = int(20 * current / total)
    bar = f"[{'█' * done}{'░' * (20 - done)}]"
    percent = (current / total) * 100
    speed = current / (now - start_time + 1)
    eta = (total - current) / speed if speed > 0 else 0

    text = (
        f"📥 Downloading...\n"
        f"{bar} {percent:.1f}%\n"
        f"**{current // (1024 * 1024)}MB / {total // (1024 * 1024)}MB**\n"
        f"ETA: `{int(eta)}s`"
    )

    try:
        asyncio.create_task(message.edit(text))
    except Exception as e:
        logging.error(f"Error updating progress: {e}")
        pass

async def processReplyToMessage(message: Message):
    msg = message.reply_to_message
    if msg and (msg.video or msg.video_note):
        m = await message.reply("⬇️ Starting download...")
        media = msg.video or msg.video_note

        file_name = getattr(media, "file_name", None) or f"{media.file_unique_id}.mp4"
        safe_file_name = clean_filename(file_name)
        file_path = f"downloads/{safe_file_name}"
        start_time = time.time()

        try:
            await app.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)
            video_original = await msg.download(file_name=file_path)
            await m.reply("✅ Download complete!")
            return video_original, m
        except Exception as e:
            logging.error(f"Download failed: {e}")
            await m.reply(f"❌ Download failed:\n`{e}`")
            return None, m
    return None, None


@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = message.from_user.mention

    if chat_id in seek_chats:
        seek_chats.pop(chat_id)

    # Handle replied video or video_note
    if message.reply_to_message and (message.reply_to_message.video or message.reply_to_message.video_note):
        input_filename, m = await processReplyToMessage(message)
        if not input_filename:
            return

        video = message.reply_to_message.video or message.reply_to_message.video_note
        video_title = message.reply_to_message.text or "Unknown"

        if chat_id in QUEUE:
            queue_num = add_to_queue(
                chat_id,
                video_title[:19],
                video.duration,
                input_filename,
                message.reply_to_message.link,
            )
            await m.edit(f"# {queue_num}\n{video_title[:19]}\nTera video queue me daal diya hu")
            return asyncio.create_task(delete_messages(message, m))

        await m.edit("Rukja...Tera Video Play kar raha hu...")

        Status, Text = await Userbot.playVideo(chat_id, input_filename)
        if not Status:
            return await m.edit(Text)

        finish_time = time.time()
        total_time_taken = str(int(finish_time - start_time)) + "s"
        await message.delete()

        await m.edit(
            f"Tera video play kar rha hu aaja vc\n\n"
            f"VideoName:- [{video_title[:19]}]({message.reply_to_message.link})\n"
            f"Duration:- {video.duration}\n"
            f"Time taken to play:- {total_time_taken}",
            disable_web_page_preview=True,
        )
        add_to_queue(chat_id, video_title[:19], video.duration, input_filename, message.reply_to_message.link)
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
    
