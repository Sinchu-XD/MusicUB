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
from Player.Utils.Loop import get_loop, set_loop
from Player.Utils.Queue import QUEUE, get_queue, clear_queue, pop_an_item



async def _skip(chat_id):
    loop = await get_loop(chat_id)
    if loop > 0:
        try:
            chat_queue = get_queue(chat_id)
            loop = loop - 1
            await set_loop(chat_id, loop)
            chat_id = chat_queue[0][0]
            duration = chat_queue[0][1][0]['title']
            songlink = chat_queue[0][2]
            link = chat_queue[0][3]
            await call.play(
                chat_id,
                MediaStream(
                    songlink,
                    video_flags=MediaStream.Flags.IGNORE,
                ),
            )
            finish_time = time.time()
            return [title, duration, link, finish_time]
        except Exception as e:
            return [2, f"Error:- <code>{e}</code>"]

    if chat_id in QUEUE:
        chat_queue = get_queue(chat_id)
        if len(chat_queue) == 1:
            await stop(chat_id)
            clear_queue(chat_id)
            return 1
        else:
            try:
                pop_an_item(chat_id)
                title = chat_queue[0][1][0]['title']
                link = chat_queue[0][2]
                songlink = chat_queue[0][3]
                # link = chat_queue[1][4]

                retry_count = 0
                max_retries = 3
                status, songlink, duration = (0, "", 0)

                while retry_count < max_retries and status == 0:
                    status, songlink = await ytdl("bestaudio", link)
                    if status == 0:
                        await asyncio.sleep(2)  # Wait before retrying
                        retry_count += 1

                duration_formatted = f"{duration // 60}:{duration % 60:02d}" if duration else "Unknown"

                if not status:
                    return [2, f"❌ **Failed to fetch next song.**"]

                await call.play(
                    chat_id,
                    MediaStream(
                        songlink,
                        video_flags=MediaStream.Flags.IGNORE,
                    ),
                )
                duration = chat_queue[0][1]['duration']
                finish_time = time.time()
                
                return [title, duration, link, finish_time]
            except Exception as e:
                return [2, f"Error:- <code>{e}</code>"]
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
        pass
    elif resp[0] == 2:
        await app.send_message(chat_id, resp[1])
    else:
        total_time_taken = str(int(start_time - resp[3])) + "s"
        await app.send_message(
            chat_id,
            f"Playing Your Song\n\nSongName:- [{resp[0]}]({resp[2]})\nDuration:- {resp[1]}\nTime taken to play:- {total_time_taken}",
            disable_web_page_preview=True,
        )


async def stop(chat_id):
    try:
        await call.leave_call(
            chat_id,
        )
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
