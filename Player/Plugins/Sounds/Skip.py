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
    start_time = time.time()
    chat_id = message.chat.id
    mention = message.from_user.mention
    if chat_id in seek_chats:
        del seek_chats[chat_id]

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
        queue_data = get_queue(chat_id)
        next_song_data = queue_data[0]
        if len(next_song_data) < 4:
            print(f"❗ Invalid song data format: {next_song_data}")
            pop_an_item(chat_id)
            return

        _chat_id, search_results, songlink, stream_url = next_song_data
        total_time = f"{int(time.time() - start_time)} **Seconds**"
   
        try:
            await Userbot.playAudio(chat_id, songlink)
        except Exception as e:
            print(f"⚠️ Error while playing next song: {e}")
            return
        await m.edit(
            f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n**SongName :** [{search_results[0]['title'][:19]}]({stream_url})\n"
            f"**Duration :** {search_results[0]['duration']} **Minutes**\n**Requested By :** {mention}\n\n**Response Time :** {total_time}\n\n\n"
            f"[**Click Here For Make Your Own Music Bot**](https://t.me/NotRealABhii)"
            ,
            disable_web_page_preview=True,
        )

        await delete_messages(message, m)
    else:
        await message.reply_text(f"❌ **You don't have permission to skip songs.** Ask an admin.\n🎤 **Skipped By**: {mention}")


@app.on_message(filters.command("queue", [PREFIX, RPREFIX]) & filters.group)
async def _queue(_, message):
    chat_id = message.chat.id
    queue = get_queue(chat_id)

    if not queue:
        return await message.reply_text("📭 **No songs in queue.**")

    output = "**🎶 Now Playing:**\n"

    # Now Playing (first song)
    try:
        current = queue[0]
        meta = current[1][0]
        output += f"▶️ [{meta['title']}]({meta['url']}) - {meta['duration']}\n"
    except Exception as e:
        output += f"▶️ Error parsing current song: {e}\n"

    # Up Next (rest of the queue)
    if len(queue) > 1:
        output += "\n**📜 Up Next:**\n"
        for i, item in enumerate(queue[1:], start=1):
            try:
                meta = item[1][0]
                output += f"{i}. [{meta['title']}]({meta['url']}) - {meta['duration']}\n"
            except Exception as e:
                output += f"{i}. ❌ Error: {e}\n"

    await message.reply_text(output, disable_web_page_preview=True)



async def stop(chat_id):
    try:
        await call.leave_call(chat_id)
    except Exception as e:
        print(f"Error stopping playback: {e}")
        
