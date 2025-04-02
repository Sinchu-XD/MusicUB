"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from Player import app, call
from Player.Core import Userbot
from Player.Utils.Queue import QUEUE, pop_an_item, get_queue, clear_queue
from Player.Utils.Loop import get_loop
from Player.Utils.Delete import delete_messages
from Player.Misc import SUDOERS
from Player.Utils.YtDetails import ytdl
from pytgcalls.types import MediaStream, VideoQuality, AudioQuality
from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
import asyncio
import time
import config

SKIP_COMMAND = ["SKIP"]
PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


@app.on_message((filters.command(SKIP_COMMAND, [PREFIX, RPREFIX])) & filters.group)
async def _aSkip(_, message):
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

        # Check if queue has next song
        if chat_id not in QUEUE or len(get_queue(chat_id)) == 1:
            clear_queue(chat_id)
            await stop(chat_id)
            return await m.edit_text(f"🚫 **Queue is empty.** Leaving voice chat...\n🎤 **Requested by:** {user_mention}")

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

        except Exception as e:
            await m.delete()
            return await app.send_message(chat_id, f"❌ **Error:** `{e}`\n🎤 **Requested by:** {user_mention}")

    else:
        return await message.reply_text(f"❌ **You don’t have permission to skip songs.** Ask an admin.\n🎤 **Requested by:** {user_mention}")
            
            
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


@app.on_message((filters.command("seek", [PREFIX, RPREFIX])) & filters.group)
async def seek_audio(_, message):
    chat_id = message.chat.id
    if chat_id not in QUEUE:
        return await message.reply_text("No song playing...")
    try:
        seek_dur = int(msg.text.split()[1])
    except:
        return await message.reply_text("Usage: /seek time (int)\n\nExample: `/seek 10`")

    chat_queue = get_queue(chat_id)
    songlink = chat_queue[0][3]
    try:
        duration = await call.time(chat_id)
        duration += seek_dur
        await call.play(
            chat_id,
            MediaStream(
                media_path=songlink,
                audio_parameters=AudioQuality.HIGH,
                video_flags=MediaStream.Flags.IGNORE,
                ffmpeg_parameters="-ss {0}".format(duration),
            ),
        )
        return await message.reply_text("Done.")
    except Exception as e:
        return await message.reply_text(f"Error: <code>{e}</code>")
