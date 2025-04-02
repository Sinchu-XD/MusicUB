
"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""
from Player import app, call
from Player.Core import Userbot
from Player.Utils.YtDetails import searchYt, extract_video_id
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Utils.Delete import delete_messages
from Player.Misc import SUDOERS

from pyrogram import filters
import os
import glob
import asyncio
import random
import time
import config

PLAY_COMMAND = ["P", "PLAY"]
PLAYFORCE_COMMAND = ["PFORCE", "PLAYFORCE"]

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


import yt_dlp

async def ytdl(link: str):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]',  # Directly downloads M4A for speed
        'geo_bypass': True,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': "cookies/cookies.txt",
        'nocheckcertificate': True,
        'outtmpl': 'downloads/%(title)s.%(ext)s',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return (1, info['url'], info.get('title', 'Unknown'), info.get('duration', 'Unknown'))
    except Exception as e:
        return (0, str(e), None, None)



async def processReplyToMessage(message):
    msg = message.reply_to_message
    if msg.audio or msg.voice:
        m = await message.reply_text("**𝓦𝓪𝓲𝓽 𝓑𝓪𝓫𝔂... 𝓓𝓸𝔀𝓷𝓵𝓸𝓪𝓭𝓲𝓷𝓰 𝓨𝓸𝓾𝓻 𝓢𝓸𝓷𝓰 ❤️**.")
        audio_original = await msg.download()
        input_filename = audio_original
        return input_filename, m
    return None



async def playWithLinks(link):
    if "&" in link:
        pass

    return 0



@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = f"[{user_name}](tg://user?id={user_id})"

    if message.reply_to_message and (message.reply_to_message.audio or message.reply_to_message.voice):
        input_filename, m = await processReplyToMessage(message)
        if input_filename is None:
            return await message.reply_text("**𝙶𝚒𝚟𝚎 𝙼𝚎 𝚂𝚘𝚗𝚐 𝙻𝚒𝚗𝚔 𝙾𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚅𝚘𝚒𝚌𝚎 𝙽𝚘𝚝𝚎😒**")
            return

        await m.edit("Processing your request...")
        Status, Text = await Userbot.playAudio(chat_id, input_filename)
        if not Status:
            return await m.edit(Text)

        await m.edit(
                    f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n**SongName**:- [{audio_title[:19]}]({message.reply_to_message.link})\n**Duration**:- {audio.duration}\n**Requested By**:- {mention}\n\n**Response Time**:- {total_time_taken}",
                    disable_web_page_preview=True,
        )

        return asyncio.create_task(delete_messages(message, m))

    elif len(message.command) < 2:
        return await message.reply_text("**𝙶𝚒𝚟𝚎 𝙼𝚎 𝚂𝚘𝚗𝚐 𝙻𝚒𝚗𝚔 𝙾𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚅𝚘𝚒𝚌𝚎 𝙽𝚘𝚝𝚎😒**")

    m = await message.reply_text("Fetching song details...")
    query = message.text.split(maxsplit=1)[1]
    video_id = extract_video_id(query)

    try:
        if video_id is None:
            video_id = query
        title, duration, link = searchYt(video_id)
        if not title:
            return await m.edit("**No results found!**")
    except Exception as e:
        return await message.reply_text(f"**Error:** `{e}`")

    await m.edit("Downloading song...")

    resp, songlink, title, duration = await ytdl(link)
    if resp == 0:
        return await m.edit(f"❌ Error fetching song\n\n`{songlink}`")

    if chat_id in QUEUE:
        queue_num = add_to_queue(chat_id, title[:19], duration, songlink, link)
        await m.edit(
            f"# {queue_num}\n{audio_title[:19]}\n**ʏᴏᴜʀ ꜱᴏɴɢ ᴀᴅᴅᴇᴅ ɪɴ Qᴜᴇᴜᴇ\nᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ 😵‍💫**"
                    )
        return asyncio.create_task(delete_messages(message, m))

    Status, Text = await Userbot.playAudio(chat_id, songlink)
    if not Status:
        return await m.edit(Text)

    finish_time = time.time()
    response_time = f"{int(finish_time - start_time)}s"

    await m.edit(
                    f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n**SongName**:- [{audio_title[:19]}]({message.reply_to_message.link})\n**Duration**:- {audio.duration}\n**Requested By**:- {mention}\n\n**Response Time**:- {total_time_taken}",
                    disable_web_page_preview=True,
                )
    asyncio.create_task(delete_messages(message, m))




@app.on_message((filters.command(PLAYFORCE_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def playforce(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = f"[{user_name}](tg://user?id={user_id})"
    
    if len(message.command) < 2:
        return await message.reply_text("**𝑊𝑎𝑖𝑡 𝙶𝚒𝚟𝚎 𝙼𝚎 𝚂𝚘𝚗𝚐 𝙻𝚒𝚗𝚔 𝙾𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚅𝚘𝚒𝚌𝚎 𝙽𝚘𝚝𝚎**")
    
    m = await message.reply_text("**Force Playing Your Song...**")
    query = message.text.split(maxsplit=1)[1]
    video_id = extract_video_id(query)
    
    try:
        if video_id is None:
            video_id = query
        title, duration, link = searchYt(video_id)
        if not title:
            return await m.edit("No results found")
    except Exception as e:
        return await message.reply_text(f"Error: <code>{e}</code>")
    
    await m.edit("**Fetching Song Details...**")
    format = "bestaudio"
    resp, songlink = await ytdl(format, link)
    if resp == 0:
        return await m.edit(f"❌ yt-dl issues detected\n\n» `{songlink}`")
    
    Status, Text = await Userbot.playAudio(chat_id, songlink)
    if Status == False:
        return await m.edit(Text)
    
    finish_time = time.time()
    total_time_taken = str(int(finish_time - start_time)) + "s"

    await m.edit(
        f"**𝑆𝑜𝑛𝑔 𝐹𝑜𝑟𝑐𝑒 𝑃𝑙𝑎𝑦𝑖𝑛𝑔 𝑖𝑛 𝑉𝐶**\n\n"
        f"**𝑆𝑜𝑛𝑔**: [{title[:19]}]({link})\n"
        f"**𝐷𝑢𝑟𝑎𝑡𝑖𝑜𝑛**: {duration}\n"
        f"**𝑅𝑒𝑞𝑢𝑒𝑠𝑡𝑒𝑑 𝐵𝑦**: {mention}\n\n"
        f"**𝑅𝑒𝑠𝑝𝑜𝑛𝑠𝑒 𝑇𝑖𝑚𝑒**: {total_time_taken}",
        disable_web_page_preview=True,
    )
    asyncio.create_task(delete_messages(message, m))


    


@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & SUDOERS)
async def _raPlay(_, message):
    start_time = time.time()
    if (message.reply_to_message) is not None:
        return await message.reply_text("Currently this is not supported")
    elif (len(message.command)) < 3:
        return await message.reply_text("You Forgot To Pass An Argument")
    else:
        m = await message.reply_text("Searching Your Query...")
        query = message.text.split(" ", 2)[2]
        msg_id = message.text.split(" ", 2)[1]
        title, duration, link = searchYt(query)
        await m.edit("Downloading...")
        format = "bestaudio"
        resp, songlink = await ytdl(format, link)
        if resp == 0:
            return await m.edit(f"❌ yt-dl issues detected\n\n» `{songlink}`")
        else:
            Status, Text = await Userbot.playAudio(msg_id, songlink)
            if Status == False:
                return await m.edit(Text)
            if duration is None:
                duration = "Playing From LiveStream"
            finish_time = time.time()
            total_time_taken = str(int(finish_time - start_time)) + "s"
            await m.edit(
                f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n**SongName**:- [{message.reply_to_message.audio.title[:19]}]({message.reply_to_message.link})\n**Duration**:- {message.reply_to_message.audio.duration}\n**Requested By**:- {mention}\n\n**Response Time**:- {total_time_taken}",
                    disable_web_page_preview=True,
            )
        asyncio.create_task(delete_messages(message, m))

