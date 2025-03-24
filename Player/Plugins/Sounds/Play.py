"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""


from Player import app, call
from Player.Core import Userbot
from Player.Utils.YtDetails import searchYt, extract_video_id
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Misc import SUDOERS

from pyrogram import filters
import os
import glob
import asyncio
import random
import time

import config

PLAY_COMMAND = ["P", "PLAY"]

PREFIX = config.PREFIX

RPREFIX = config.RPREFIX



async def ytdl(format: str, link: str):
    cookie_path = "cookies/cookies.txt"  # Ensure this matches the correct path
    stdout, stderr = await bash(
        f'yt-dlp --geo-bypass --cookies "{cookie_path}" -g -f "{format}" {link}'
    )
    if stdout:
        return 1, stdout
    return 0, stderr



async def bash(cmd):
    process = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await process.communicate()
    err = stderr.decode().strip()
    out = stdout.decode().strip()
    return out, err


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
    if "?" in link:
        pass

    return 0


@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    mention = f"[{user_name}](tg://user?id={user_id})"
    if (message.reply_to_message) is not None:
        if message.reply_to_message.audio or message.reply_to_message.voice:
            input_filename, m = await processReplyToMessage(message)
            if input_filename is None:
                return await message.reply_text(
                    "**𝙶𝚒𝚟𝚎 𝙼𝚎 𝚂𝚘𝚗𝚐 𝙻𝚒𝚗𝚔 𝙾𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚅𝚘𝚒𝚌𝚎 𝙽𝚘𝚝𝚎😒**"
                )
                
            await m.edit("𝑊𝑎𝑖𝑡 𝑁𝑎 𝑌𝑟𝑟𝑟 😒..")
            Status, Text = await Userbot.playAudio(chat_id, input_filename)
            if Status == False:
                await m.edit(Text)
            else:
                audio = message.reply_to_message.audio or message.reply_to_message.voice
                audio_title = message.reply_to_message.text or "Unknown"
                if chat_id in QUEUE:
                    queue_num = add_to_queue(
                        chat_id,
                        audio_title[:19],
                        audio.duration,
                        audio.file_id,
                        message.reply_to_message.link,
                    )
                    return await m.edit(
                        f"# {queue_num}\n{audio_title[:19]}\n**ʏᴏᴜʀ ꜱᴏɴɢ ᴀᴅᴅᴇᴅ ɪɴ Qᴜᴇᴜᴇ\nᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ 😵‍💫**"
                    )
                finish_time = time.time()
                total_time_taken = str(int(finish_time - start_time)) + "s"
                await m.edit(
                    f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n**SongName**:- [{audio_title[:19]}]({message.reply_to_message.link})\n**Duration**:- {audio.duration}\n**Requested By**:- {mention}\n\n**Response Time**:- {total_time_taken}",
                    disable_web_page_preview=True,
                )
    elif (len(message.command)) < 2:
        await message.reply_text("**𝑊𝑎𝑖𝑡 𝙶𝚒𝚟𝚎 𝙼𝚎 𝚂𝚘𝚗𝚐 𝙻𝚒𝚗𝚔 𝙾𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚅𝚘𝚒𝚌𝚎 𝙽𝚘𝚝𝚎**")
    else:
        m = await message.reply_text("**Wait Na Yrrr 😒**")
        query = message.text.split(maxsplit=1)[1]
        video_id = extract_video_id(query)
        try:
            if video_id is None:
                video_id = query
            title, duration, link = searchYt(video_id)
            if (title, duration, link) == (None, None, None):
                await m.edit("No results found")
        except Exception as e:
            return await message.reply_text(f"Error:- <code>{e}</code>")

        await m.edit("**ᴡᴀɪᴛ ɴᴀ ʏʀʀʀ\n\nꜱᴇᴀʀᴄʜɪɴɢ ʏᴏᴜʀ ꜱᴏɴɢ 🌚❤️..**")
        format = "bestaudio"
        resp, songlink = await ytdl(format, link)
        if resp == 0:
            await m.edit(f"❌ yt-dl issues detected\n\n» `{songlink}`")
        else:
            if chat_id in QUEUE:
                queue_num = add_to_queue(chat_id, title[:19], duration, songlink, link)
                await m.edit(
                    f"# {queue_num}\n{title[:19]}\n**ʏᴏᴜʀ ꜱᴏɴɢ ᴀᴅᴅᴇᴅ ɪɴ Qᴜᴇᴜᴇ\n\nᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ 😵‍💫**"
                )
                await asyncio.sleep(5)
                return await m.delete()
            Status, Text = await Userbot.playAudio(chat_id, songlink)
            if Status == False:
                return await m.edit(Text)
            if duration is None:
                duration = "**Playing From LiveStream**"
            add_to_queue(chat_id, title[:19], duration, songlink, link)
            finish_time = time.time()
            total_time_taken = str(int(finish_time - start_time)) + "s"
            await m.edit(
                f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n**SongName**:- [{title[:19]}]({link})\n**Duration**:- {duration}\n**Requested By**:- {mention}\n\n**Respose Time**:- {total_time_taken}",
                disable_web_page_preview=True,
            )
        await asyncio.sleep(2)
        await m.delete()


    


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
        await asyncio.sleep(2)
        await m.delete()
