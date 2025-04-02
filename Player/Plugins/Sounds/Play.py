from Player import app, call
from Player.Core import Userbot
from Player.Utils.YtDetails import searchYt, extract_video_id
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Misc import SUDOERS

from pyrogram import filters
import asyncio
import time
import config

PLAY_COMMAND = ["P", "PLAY"]
PLAYFORCE_COMMAND = ["PFORCE", "PLAYFORCE"]

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


async def ytdl(format: str, link: str):
    cookie_path = "cookies/cookies.txt"
    stdout, stderr = await bash(
        f'yt-dlp --geo-bypass --cookies "{cookie_path}" -g -f "{format}" {link}'
    )
    return (1, stdout) if stdout else (0, stderr)


async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return stdout.decode().strip(), stderr.decode().strip()


async def play_song(chat_id, song_title, song_link, requested_by):
    """Handles playing a new song and resetting queue after VC restarts."""
    if chat_id in QUEUE:
        QUEUE[chat_id].clear()  # Reset queue after VC restarts

    QUEUE[chat_id] = [{
        "title": song_title,
        "link": song_link,
        "requested_by": requested_by
    }]

    # Ensure VC is connected before playing
    if not call.is_connected(chat_id):
        await call.start(chat_id)
        await asyncio.sleep(2)

    Status, Text = await Userbot.playAudio(chat_id, song_link)
    if Status:
        await app.send_message(
            chat_id,
            f"**🎶 Now Playing...**\n\n"
            f"**Song Name:** [{song_title}]({song_link})\n"
            f"**Requested By:** {requested_by}",
            disable_web_page_preview=True
        )
    else:
        await app.send_message(chat_id, f"❌ Error playing song: {Text}")


@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def play_command(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = f"[{user_name}](tg://user?id={user_id})"

    if len(message.command) < 2:
        return await message.reply_text("**Please provide a song name or link.**")

    m = await message.reply_text("**Searching for your song... 🎶**")
    query = message.text.split(maxsplit=1)[1]
    video_id = extract_video_id(query)

    try:
        if video_id is None:
            video_id = query
        title, duration, link = searchYt(video_id)
        if not title:
            return await m.edit("No results found.")
    except Exception as e:
        return await m.edit(f"Error: <code>{e}</code>")

    await m.edit("**Downloading the song... 🎧**")
    format = "bestaudio"
    resp, songlink = await ytdl(format, link)

    if resp == 0:
        return await m.edit(f"❌ yt-dl issues detected\n\n» `{songlink}`")

    await play_song(chat_id, title[:19], songlink, mention)

    finish_time = time.time()
    total_time_taken = str(int(finish_time - start_time)) + "s"
    
    await m.edit(
        f"**🎵 Song is now playing in VC!**\n\n"
        f"**Song Name:** [{title[:19]}]({link})\n"
        f"**Duration:** {duration}\n"
        f"**Requested By:** {mention}\n\n"
        f"**Response Time:** {total_time_taken}",
        disable_web_page_preview=True,
    )
    await asyncio.sleep(2)
    await m.delete()


@app.on_message((filters.command(PLAYFORCE_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def playforce_command(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = f"[{user_name}](tg://user?id={user_id})"

    if len(message.command) < 2:
        return await message.reply_text("**Please provide a song name or link.**")

    m = await message.reply_text("**Force Playing Your Song... 🔥**")
    query = message.text.split(maxsplit=1)[1]
    video_id = extract_video_id(query)

    try:
        if video_id is None:
            video_id = query
        title, duration, link = searchYt(video_id)
        if not title:
            return await m.edit("No results found.")
    except Exception as e:
        return await m.edit(f"Error: <code>{e}</code>")

    await m.edit("**Downloading the song... 🎧**")
    format = "bestaudio"
    resp, songlink = await ytdl(format, link)

    if resp == 0:
        return await m.edit(f"❌ yt-dl issues detected\n\n» `{songlink}`")

    await play_song(chat_id, title[:19], songlink, mention)

    finish_time = time.time()
    total_time_taken = str(int(finish_time - start_time)) + "s"
    
    await m.edit(
        f"**🎵 Song is now playing in VC!**\n\n"
        f"**Song Name:** [{title[:19]}]({link})\n"
        f"**Duration:** {duration}\n"
        f"**Requested By:** {mention}\n\n"
        f"**Response Time:** {total_time_taken}",
        disable_web_page_preview=True,
    )
    await asyncio.sleep(2)
    await m.delete()





@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & SUDOERS)
async def admin_play(_, message):
    start_time = time.time()
    
    if len(message.command) < 3:
        return await message.reply_text("**You forgot to pass an argument!**")
    
    m = await message.reply_text("**Searching for your query...**")
    query = message.text.split(" ", 2)[2]
    msg_id = message.text.split(" ", 2)[1]
    
    title, duration, link = searchYt(query)
    
    await m.edit("**Downloading...**")
    format = "bestaudio"
    resp, songlink = await ytdl(format, link)
    
    if resp == 0:
        return await m.edit(f"❌ yt-dl issues detected\n\n» `{songlink}`")
    
    await play_song(msg_id, title[:19], songlink, "Admin")
    
    finish_time = time.time()
    total_time_taken = str(int(finish_time - start_time)) + "s"
    
    await m.edit(
        f"**🎵 Song is now playing in VC!**\n\n"
        f"**Song Name:** [{title[:19]}]({link})\n"
        f"**Duration:** {duration}\n"
        f"**Requested By:** Admin\n\n"
        f"**Response Time:** {total_time_taken}",
        disable_web_page_preview=True,
    )
    await asyncio.sleep(2)
    await m.delete()
