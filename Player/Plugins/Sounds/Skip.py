import logging
import time
import asyncio
import config
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
from pytgcalls.types import MediaStream

from Player import app, call, seek_chats
from Player.Core import Userbot
from Player.Misc import SUDOERS
from Player.Utils.Loop import get_loop
from Player.Utils.YtDetails import ytdl
from Player.Utils.Delete import delete_messages
from Player.Utils.Queue import QUEUE, get_queue, pop_an_item, clear_queue, add_to_queue #process_next_song

from pyrogram import filters

logging.basicConfig(level=logging.INFO)

SKIP_COMMAND = ["SKIP"]
PREFIX = config.PREFIX
RPREFIX = config.RPREFIX

@app.on_message((filters.command(SKIP_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def skip_song(_, message):
    chat_id = message.chat.id
    if chat_id in seek_chats:
        del seek_chats[chat_id]
    start_time = time.time()
    mention = message.from_user.mention

    admins = []
    async for admin in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        admins.append(admin.user.id)
    if message.from_user.id in SUDOERS or message.from_user.id in admins:
        m = await message.reply_text(f"⏩ **Skipping song...**\n🎤 **Skipped By**:{mention}")

        if await get_loop(chat_id) != 0:
            await m.edit_text(f"🔄 **Loop is enabled!** Disable it with `{config.PREFIX}endloop` to skip.\n🎤 **Skipped By**: {mention}")
            await delete_messages(message, m)
            return

        if chat_id not in QUEUE or len(get_queue(chat_id)) == 1:
            clear_queue(chat_id)
            await stop(chat_id)
            await m.edit_text(f"🚫 **Queue is empty.** Leaving voice chat...\n🎤 **Skipped By**: {mention}")
            await delete_messages(message, m)
            return

        pop_an_item(chat_id)
        await process_next_song(chat_id)

        await delete_messages(message, m)
    else:
        await message.reply_text(f"❌ **You don't have permission to skip songs.** Ask an admin.\n🎤 **Skipped By**: {mention}")

async def process_next_song(chat_id):
    queue_data = get_queue(chat_id)
    if not queue_data:
        print(f"Queue empty at process_next_song: {chat_id}")
        return

    next_song_data = queue_data[0]

    if len(next_song_data) != 4:
        print(f"❗ Wrong song data format: {next_song_data}")
        pop_an_item(chat_id)  # Remove broken data
        await process_next_song(chat_id)
        return

    try:
        chat_id_in_queue, search_results, songlink, stream_url = next_song_data
    except Exception as e:
        print(f"Unpacking error: {e}")
        pop_an_item(chat_id)
        await process_next_song(chat_id)
        return

    try:
        print(f"Processing next song: {stream_url}")
        result = await ytdl("bestaudio", stream_url)
        if not result or len(result) != 2:
            print(f"ytdl failed for {stream_url}")
            pop_an_item(chat_id)
            await process_next_song(chat_id)
            return

        resp, new_songlink = result
        if resp != 0 or not new_songlink:
            print(f"Stream fetch failed for {stream_url}")
            pop_an_item(chat_id)
            await process_next_song(chat_id)
            return

        await Userbot.playAudio(chat_id, new_songlink)

    except Exception as e:
        print(f"Error playing next song: {e}")
        pop_an_item(chat_id)
        await process_next_song(chat_id)

@app.on_message(filters.command("queue", [PREFIX, RPREFIX]) & filters.group)
async def _queue(_, message):
    chat_id = message.chat.id
    if chat_id in QUEUE and len(get_queue(chat_id)) > 1:
        queue = get_queue(chat_id)[1:]
        output = "**🎵 Queue:**\n"
        for i, item in enumerate(queue):
            title = item[1]
            duration = item[2]
            link = item[3]
            output += f"{i + 1}. [{title}]({link}) - {duration}\n"
        await message.reply_text(output, disable_web_page_preview=True)
    else:
        await message.reply_text("⚠️ Queue is empty!")
        
async def stop(chat_id):
    try:
        await call.leave_call(chat_id)
    except Exception as e:
        print(f"Error stopping playback: {e}")
        
