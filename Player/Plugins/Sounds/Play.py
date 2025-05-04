"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""
from Player import app, call, seek_chats
from Player.Core import Userbot
from Player.Utils.YtDetails import SearchYt, ytdl
from Player.Utils.Spotify import spotify_search
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Utils.Delete import delete_messages
from pyrogram.enums import ChatMembersFilter
from Player.Misc import SUDOERS
from pyrogram import filters
import os
import re
import asyncio
import time
import hashlib
import logging
import config

PLAY_COMMAND = ["P", "PLAY", "SP", "SPLAY"]
PLAYFORCE_COMMAND = ["PFORCE", "PLAYFORCE"]
PREFIX = config.PREFIX
RPREFIX = config.RPREFIX
YOUTUBE_REGEX = r"^(https?\:\/\/)?(www\.youtube\.com|youtu\.?be)\/.+"

async def processReplyToMessage(message):
    msg = message.reply_to_message
    if msg.audio or msg.voice:
        m = await message.reply_text("**𝓦𝓪𝓲𝓽 𝓑𝓪𝓫𝔂... 𝓓𝓸𝔀𝓷𝓵𝓸𝓪𝓭𝓲𝓷𝓰 𝓨𝓸𝓾𝓻 𝓢𝓸𝓷𝓰 ❤️**.")
        audio_original = await msg.download()
        return audio_original, m
    return None, None

@app.on_message((filters.command(PLAY_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = message.from_user.mention
    command = message.command[0].lower()
    await message.delete()

    if chat_id in seek_chats:
        del seek_chats[chat_id]

    if message.reply_to_message:
        input_filename, m = await processReplyToMessage(message)
        if input_filename is None:
            return await message.reply_text(
                "**𝙶𝚒𝚟𝚎 𝙼𝚎 𝚂𝚘𝚗𝚐 𝙻𝚒𝚗𝚔 𝙾𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚅𝚘𝚒𝚌𝚎 𝙽𝚘𝚝𝚎😒**"
            )

        await m.edit("𝑊𝑎𝑖𝑡 𝑁𝑎 𝑌𝑟𝑟𝑟 😒..")
        Status, Text = await Userbot.playAudio(chat_id, input_filename)
        if not Status:
            return await m.edit(Text)

        audio = message.reply_to_message.audio or message.reply_to_message.voice
        audio_title = message.reply_to_message.text or "Unknown"
        if chat_id in QUEUE:
            queue_num = add_to_queue(chat_id, audio_title[:19], audio.duration, audio.file_id, message.reply_to_message.link)
            await m.edit(f"# {queue_num}\n{audio_title[:19]}\n**ʏᴏᴜʀ ꜱᴏɴɢ ᴀᴅᴅᴇᴅ ɪɴ Qᴜᴇᴜᴇ\nᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ 😵‍💫**")
            return asyncio.create_task(delete_messages(message, m))

        total_time = f"{int(time.time() - start_time)} **Seconds**"
        await m.edit(
            f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n**SongName**:- [{audio_title[:19]}]({message.reply_to_message.link})\n"
            f"**Duration**:- {audio.duration}\n**Requested By**:- {mention}\n\n**Response Time**:- {total_time}",
            disable_web_page_preview=True,
        )
        return asyncio.create_task(delete_messages(message, m))

    elif len(message.command) < 2:
        return await message.reply_text("**𝑊𝑎𝑖𝑡 𝙶𝚒𝚟𝚎 𝙼𝚎 𝚂𝚘𝚗𝚐 𝙻𝚒𝚗𝚔 𝙾𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚅𝚘𝚒𝚌𝚎 𝙽𝚘𝚝𝚎**")

    else:
        m = await message.reply_text("**Wait Na Yrrr 😒**")
    query = message.text.split(maxsplit=1)[1]
    
    if re.match(YOUTUBE_REGEX, query):
    stream_url = query
    await m.edit("**𝑾𝒂𝒊𝒕... 𝑫𝒐𝒘𝒏𝒍𝒐𝒂𝒅𝒊𝒏𝒈 𝒅𝒊𝒓𝒆𝒄𝒕 𝒍𝒊𝒏𝒌...**")
    try:
        result = await ytdl("bestaudio", stream_url)
        resp, songlink = result[0], result[1]
        if not resp or not songlink:
            return await m.edit("❌ yt-dl failed to fetch direct audio.")

    except Exception as e:
        return await m.edit(f"**yt-dl error:** <code>{e}</code>")
else:

    try:
        search_results, stream_url = await SearchYt(query)
        if not search_results:
            return await m.edit("No results found")
    except Exception as e:
        return await m.edit(f"Error: <code>{e}</code>")

    await m.edit("**ᴡᴀɪᴛ ɴᴀ ʏʀʀʀ\n\nꜱᴇᴀʀᴄʜɪɴɢ ʏᴏᴜʀ ꜱᴏɴɢ 🌚❤️..**")
    
    status, songlink = await ytdl("bestaudio", stream_url)
    print(songlink)
    if not status or not songlink:
        await m.edit(f"❌ yt-dl issues detected\n\n» No valid song link found.")
    else:
        title = search_results[0]['title']
        chat_id = message.chat.id
        total_time = f"{int(time.time() - start_time)} **Seconds**"
                if chat_id in QUEUE:
            queue_num = add_to_queue(chat_id, search_results, songlink, stream_url)
            await m.edit(
                f"# **{queue_num} ʏᴏᴜʀ ꜱᴏɴɢ ᴀᴅᴅᴇᴅ ɪɴ Qᴜᴇᴜᴇ\n\nᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ 😵‍💫**\n\n"
                f"**SongName :** [{search_results[0]['title'][:19]}]({stream_url})\n"
                f"**Duration :** {search_results[0]['duration']} **Minutes**\n"
                f"**Channel :** {search_results[0]['channel']}\n"
                f"**Views :** {search_results[0]['views']}\n"
                f"**Requested By :** {mention}\n\n"
                f"**Response Time :** {total_time}",
                disable_web_page_preview=True,
            )
                
                
            asyncio.create_task(delete_messages(message, m))
            return

        Status, Text = await Userbot.playAudio(chat_id, songlink)
        if not Status:
            return await m.edit(Text)

        add_to_queue(chat_id, search_results, songlink, stream_url)
        total_time = f"{int(time.time() - start_time)} **Seconds**"
        await m.edit(
            f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n**SongName :** [{search_results[0]['title'][:19]}]({stream_url})\n"
            f"**Duration :** {search_results[0]['duration']} **Minutes**\n**Channel :** {search_results[0]['channel']}\n"
            f"**Views :** {search_results[0]['views']}\n**Requested By :** {mention}\n\n**Response Time :** {total_time}",
        asyncio.create_task(delete_messages(message, m))
        return
            

@app.on_message((filters.command(PLAYFORCE_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def playforce(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = message.from_user.mention
    await message.delete()

    seek_chats.pop(chat_id, None)

    if len(message.command) < 2:
        return await message.reply_text("**𝑊𝑎𝑖𝑡 𝙶𝚒𝚟𝚎 𝙼𝚎 𝚂𝚘𝚗𝚐 𝙻𝚒𝚗𝚔 𝙾𝚛 𝚁𝚎𝚙𝚕𝚢 𝚃𝚘 𝚅𝚘𝚒𝚌𝚎 𝙽𝚘𝚝𝚎**")
    
    admins = [admin.user.id async for admin in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS)]

    if message.from_user.id not in SUDOERS and message.from_user.id not in admins:
        return await message.reply_text("**Only Admins or SUDO Users can use Force Play!**")
    m = await message.reply_text("**Force Playing Your Song...**")
    query = message.text.split(maxsplit=1)[1]

    try:
        search_results, stream_url = await SearchYt(query)
        if not search_results:
            return await m.edit("No results found.")
    except Exception as e:
        return await m.edit(f"Error while searching: <code>{e}</code>")

    await m.edit("**Fetching Song Details...**")

    try:
        result = await ytdl("bestaudio", stream_url)
        resp = result[0]
        songlink = result[1]
        duration = search_results[0]['duration']
    except Exception as e:
        return await m.edit(f"Error while downloading: <code>{e}</code>")

    if resp == 0 or not songlink:
        return await m.edit("❌ yt-dl issues detected.\n\n» No valid song link found.")

    QUEUE[chat_id] = [(search_results[0]['title'], message.from_user.id, songlink)]
    seek_chats.pop(chat_id, None)

    Status, Text = await Userbot.playAudio(chat_id, songlink)
    if not Status:
        return await m.edit(Text)

    total_time = f"{int(time.time() - start_time)} **Seconds**"
    await m.edit(
        f"**𝑆𝑜𝑛𝑔 𝐹𝑜𝑟𝑐𝑒 𝑃𝑙𝑎𝑦𝑒𝑑 𝑎𝑡 ν𝑐**\n\n"
        f"**SongName :** [{search_results[0]['title'][:19]}]({stream_url})\n"
        f"**Duration :** {duration} **Minutes**\n\n"
        f"**Channel :** {search_results[0]['channel']}\n"
        f"**Views :** {search_results[0]['views']}\n"
        f"**Requested By :** {mention}\n\n"
        f"**Response Time :** {total_time}",
        disable_web_page_preview=True,
    )
    return asyncio.create_task(delete_messages(message, m))
