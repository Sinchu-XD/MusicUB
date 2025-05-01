"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import time
import asyncio
from pytgcalls import PyTgCalls, filters
from pytgcalls.types import Update, MediaStream, ChatUpdate

from Player import call, app, seek_chats
from Player.Utils.YtDetails import ytdl
from Player.Utils.Seek_Bar import update_seek_bar
from Player.Utils.AutoPlay import is_autoplay_on, get_recommendation
from Player.Utils.Loop import get_loop, set_loop
from Player.Utils.Queue import QUEUE, get_queue, clear_queue, pop_an_item


async def _skip(chat_id):
    loop = await get_loop(chat_id)
    if loop > 0:
        try:
            chat_queue = get_queue(chat_id)
            loop -= 1
            await set_loop(chat_id, loop)
            current = chat_queue[0]
            title = current[1][0]['title']
            duration = current[1][0]['duration']
            channel = current[1][0]['channel']
            views = current[1][0]['views']
            songlink = current[2]
            ytlink = current[3]

            await call.play(chat_id, MediaStream(songlink, video_flags=MediaStream.Flags.IGNORE))
            start_time = time.time()
            await update_seek_bar(chat_id, duration, start_time, title, ytlink, channel, views)

            finish_time = time.time()
            return [title, duration, channel, views, ytlink, finish_time]
        except Exception as e:
            return [2, f"❌ **Loop Play Failed:**\n`{e}`"]

    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await stop(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            try:
                pop_an_item(chat_id)
                next_song = chat_queue[0]
                title = next_song[1][0]['title']
                duration = next_song[1][0]['duration']
                channel = next_song[1][0]['channel']
                views = next_song[1][0]['views']
                songlink = next_song[2]
                ytlink = next_song[3]
                
                await call.play(chat_id, MediaStream(songlink, video_flags=MediaStream.Flags.IGNORE))
                start_time = time.time()
                await update_seek_bar(chat_id, duration, start_time, title, ytlink, channel, views)

                finish_time = time.time()
                return [title, duration, channel, views, ytlink, finish_time]
            except Exception as e:
                return [2, f"❌ **Skip Error:** `{e}`"]

    await stop(chat_id)
    return 1


@call.on_update(filters.stream_end())
async def handler(client: PyTgCalls, update: Update):
    start_time = time.time()
    chat_id = update.chat_id

    if chat_id in seek_chats:
        del seek_chats[chat_id]

    resp = await _skip(chat_id)

    if resp == 1:
        return

    if resp[0] == 2:
        await app.send_message(chat_id, resp[1])
    else:
        total_time = int(time.time() - resp[5])
        m = await app.send_message(
            chat_id,
            f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n"
            f"**SongName :** [{resp[0][:19]}]({resp[4]})\n"
            f"**Duration :** {resp[1]} **Minutes**\n"
            f"**Channel :** {resp[2]}\n"
            f"**Views :** {resp[3]}\n\n"
            f"**Response Time :** `{total_time}` **Seconds**",
            disable_web_page_preview=True,
        )
        await asyncio.sleep(10)
        await m.delete()


async def stop(chat_id):
    try:
        await call.leave_call(chat_id)
    except:
        pass


@call.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
async def on_left_call(client, update):
    chat_id = update.chat_id
    await stop(chat_id)
    clear_queue(chat_id)
    await set_loop(chat_id, 0)
    if chat_id in seek_chats:
        del seek_chats[chat_id]
        
