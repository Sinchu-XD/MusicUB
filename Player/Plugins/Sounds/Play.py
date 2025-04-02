
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

async def ytdl(format: str, link: str):
    ydl_opts = {
        'format': format,
        'geo_bypass': True,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': "cookies/cookies.txt",
        'nocheckcertificate': True,
        'extract_flat': True,  # Prevents unnecessary metadata downloads
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            return (1, info['url']) if 'url' in info else (0, "No URL found")
    except Exception as e:
        return (0, str(e))


async def processReplyToMessage(message):
    msg = message.reply_to_message
    if msg.audio or msg.voice:
        m = await message.reply_text("Rukja...Tera Audio Download kar raha hu...")
        audio_original = await msg.download()
        input_filename = audio_original
        return input_filename, m
    return None


async def playWithLinks(link):
    if "&" in link:
        pass
    if "?" in link:
        pass

    return 0


@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    if (message.reply_to_message) is not None:
        if message.reply_to_message.audio or message.reply_to_message.voice:
            input_filename, m = await processReplyToMessage(message)
            if input_filename is None:
                await message.reply_text(
                    "Audio pe reply kon karega mai? ya phir song link kon dalega mai? 🤔"
                )
                return
            await m.edit("Rukja...Tera Audio Play karne vala hu...")
            Status, Text = await Userbot.playAudio(chat_id, input_filename)
            if Status == False:
                await m.edit(Text)
            else:
                if chat_id in QUEUE:
                    queue_num = add_to_queue(
                        chat_id,
                        message.reply_to_message.audio.title[:19],
                        message.reply_to_message.audio.duration,
                        message.reply_to_message.audio.file_id,
                        message.reply_to_message.link,
                    )
                    await m.edit(
                        f"# {queue_num}\n{message.reply_to_message.audio.title[:19]}\nTera gaana queue me daal diya hu"
                    )
                    return
                finish_time = time.time()
                total_time_taken = str(int(finish_time - start_time)) + "s"
                await m.edit(
                    f"Tera gaana play kar rha hu aaja vc\n\nSongName:- [{message.reply_to_message.audio.title[:19]}]({message.reply_to_message.link})\nDuration:- {message.reply_to_message.audio.duration}\nTime taken to play:- {total_time_taken}",
                    disable_web_page_preview=True,
                )
    elif (len(message.command)) < 2:
        await message.reply_text("Song name kon dalega mai? 🤔")
    else:
        m = await message.reply_text("Rukja...Tera gaana dhund raha hu...")
        query = message.text.split(maxsplit=1)[1]
        video_id = extract_video_id(query)
        try:
            if video_id is None:
                video_id = query
            title, duration, link = searchYt(video_id)
            if (title, duration, link) == (None, None, None):
                return await m.edit("No results found")
        except Exception as e:
            await message.reply_text(f"Error:- <code>{e}</code>")
            return

        await m.edit("Rukja...Tera gaana download kar raha hu...")
        format = "bestaudio"
        resp, songlink = await ytdl(format, link)
        if resp == 0:
            await m.edit(f"❌ yt-dl issues detected\n\n» `{songlink}`")
        else:
            if chat_id in QUEUE:
                queue_num = add_to_queue(chat_id, title[:19], duration, songlink, link)
                await m.edit(
                    f"# {queue_num}\n{title[:19]}\nTera gaana queue me daal diya hu"
                )
                return
            # await asyncio.sleep(1)
            Status, Text = await Userbot.playAudio(chat_id, songlink)
            if Status == False:
                await m.edit(Text)
            if duration is None:
                duration = "Playing From LiveStream"
            add_to_queue(chat_id, title[:19], duration, songlink, link)
            finish_time = time.time()
            total_time_taken = str(int(finish_time - start_time)) + "s"
            await m.edit(
                f"Tera gaana play kar rha hu aaja vc\n\nSongName:- [{title[:19]}]({link})\nDuration:- {duration}\nTime taken to play:- {total_time_taken}",
                disable_web_page_preview=True,
            )




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
    
    add_to_queue(chat_id, title[:19], duration, songlink, link)
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

