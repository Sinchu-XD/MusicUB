"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import time
import config
import asyncio

from Player import app, call, seek_chats
from Player.Core import Userbot
from Player.Misc import SUDOERS
from Player.Utils.Loop import get_loop
from Player.Utils.YtDetails import ytdl
from Player.Utils.Delete import delete_messages
from Player.Utils.Queue import QUEUE, pop_an_item, get_queue, clear_queue

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter

from pytgcalls.types import MediaStream

SKIP_COMMAND = ["SKIP"]
PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


@app.on_message((filters.command(SKIP_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aSkip(_, message):
    if chat_id in seek_chats:
        del seek_chats[chat_id]
    start_time = time.time()
    chat_id = message.chat.id
    user_mention = message.from_user.mention

    # Check if user has permission to skip
    administrators = []
    async for m in app.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        administrators.append(m)

    if message.from_user.id in SUDOERS or message.from_user.id in [admin.user.id for admin in administrators]:
        m = await message.reply_text(f"⏩ **Skipping song...**\n🎤 Requested by: {user_mention}")

        # Check if looping is enabled
        loop = await get_loop(chat_id)
        if loop != 0:
            return await m.edit_text(
                f"🔄 **Loop is enabled!** Disable it with `{PREFIX}endloop` to skip.\n🎤 **Requested by:** {user_mention}"
            )
            asyncio.create_task(delete_messages(message, m))

        # Check if queue has next song
        if chat_id not in QUEUE or len(get_queue(chat_id)) == 1:
            clear_queue(chat_id)
            await stop(chat_id)
            return await m.edit_text(f"🚫 **Queue is empty.** Leaving voice chat...\n🎤 **Requested by:** {user_mention}")
            asyncio.create_task(delete_messages(message, m))

        try:
            # Fetch next song details
            next_song_data = get_queue(chat_id)[1]
            title = next_song_data[1]
            link = next_song_data[3]

            # Try fetching the audio URL and duration
            retry_count = 0
            max_retries = 3
            status, songlink, duration = (0, "", 0)

            while retry_count < max_retries and status == 0:
                status, songlink, duration = await ytdl("bestaudio", link)
                if status == 0:
                    await asyncio.sleep(2)  # Wait before retrying
                    retry_count += 1

            if not status:
                return await m.edit_text(f"❌ **Failed to fetch next song.**\n🛑 `{songlink}`\n🎤 **Requested by:** {user_mention}")
                asyncio.create_task(delete_messages(message, m))

            # Convert duration to readable format (MM:SS)
            duration_formatted = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"

            # Play next song
            await call.play(
                chat_id,
                MediaStream(songlink, video_flags=MediaStream.Flags.AUTO_DETECT),
            )

            # Remove skipped song from queue
            pop_an_item(chat_id)

            # Time calculation
            finish_time = time.time()
            total_time_taken = f"{int(finish_time - start_time)}s"

            await m.delete()
            await app.send_message(
                chat_id,
                f"🎶 **Now Playing:** [{title}]({link})\n"
                f"⏳ **Duration:** {duration_formatted}\n"
                f"⚡ **Time Taken:** {total_time_taken}\n"
                f"🎤 **Requested by:** {user_mention}",
                disable_web_page_preview=True,
            )
            asyncio.create_task(delete_messages(message, m))

        except Exception as e:
            await m.delete()
            return await app.send_message(chat_id, f"❌ **Error:** `{e}`\n🎤 **Requested by:** {user_mention}")

    else:
        return await message.reply_text(f"❌ **You don’t have permission to skip songs.** Ask an admin.\n🎤 **Requested by:** {user_mention}")
        asyncio.create_task(delete_messages(message, m))
            
            
@app.on_message(filters.command("queue", [PREFIX, RPREFIX]) & filters.group)
async def _queue(_, message):
    chat_id = message.chat.id
    if chat_id in QUEUE and len(get_queue(chat_id)) > 1:
        queue = get_queue(chat_id)[1:]
        output = "**🎵 Queue:**\n"
        for i, item in enumerate(queue):
            title = item[1]
            duration = item[2]
            link = item[4]
            output += f"{i + 1}. [{title}]({link}) - {duration}\n"
        await message.reply_text(output, disable_web_page_preview=True)
    else:
        await message.reply_text("⚠️ Queue is empty!")
        


async def stop(chat_id):
    try:
        await call.leave_call(chat_id)
    except:
        pass
