"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import asyncio
import time
import logging
from pytgcalls.types import Update, MediaStream, ChatUpdate
from pytgcalls import PyTgCalls, filters

from Player import call, app, seek_chats
from Player.Utils.Loop import get_loop, set_loop
from Player.Utils.Queue import QUEUE, get_queue, clear_queue, pop_an_item

logging.basicConfig(level=logging.INFO)

# ─────────────────────────────
# SKIP / NEXT SONG HANDLER
# ─────────────────────────────
async def _skip(chat_id):
    loop = await get_loop(chat_id)
    chat_queue = get_queue(chat_id)

    # 🔴 NO QUEUE → FULL STOP
    if not chat_queue:
        await stop(chat_id)
        return 1

    # 🔁 LOOP MODE
    if loop > 0:
        try:
            await set_loop(chat_id, loop - 1)
            current = chat_queue[0]

            title = current[1][0]['title']
            duration = current[1][0]['duration']
            channel = current[1][0]['channel']
            views = current[1][0]['views']
            songlink = current[2]
            ytlink = current[3]

            await call.play(
                chat_id,
                MediaStream(songlink, video_flags=MediaStream.Flags.IGNORE)
            )

            finish_time = time.time()
            return [title, duration, channel, views, ytlink, finish_time]

        except Exception as e:
            return [2, f"❌ **Loop Play Failed:** `{e}`"]

    # ⏭ NORMAL SKIP
    if chat_id in QUEUE:
        if len(chat_queue) == 1:
            # 🔥 LAST SONG → HARD CLEAN
            await stop(chat_id)
            clear_queue(chat_id)
            await set_loop(chat_id, 0)
            return 1

        try:
            pop_an_item(chat_id)
            chat_queue = get_queue(chat_id)

            if not chat_queue:
                await stop(chat_id)
                return 1

            next_song = chat_queue[0]

            title = next_song[1][0]['title']
            duration = next_song[1][0]['duration']
            channel = next_song[1][0]['channel']
            views = next_song[1][0]['views']
            songlink = next_song[2]
            ytlink = next_song[3]

            await call.play(
                chat_id,
                MediaStream(songlink, video_flags=MediaStream.Flags.IGNORE)
            )

            finish_time = time.time()
            return [title, duration, channel, views, ytlink, finish_time]

        except Exception as e:
            return [2, f"❌ **Skip Error:** `{e}`"]

    await stop(chat_id)
    return 1


# ─────────────────────────────
# STREAM END EVENT (FIXED)
# ─────────────────────────────
@call.on_update(filters.stream_end())
async def handler(_: PyTgCalls, update: Update):
    chat_id = update.chat_id

    # 🧹 clear seek
    if chat_id in seek_chats:
        del seek_chats[chat_id]

    resp = await _skip(chat_id)

    # 🔥 IF VC END → CLEAN MEMORY
    if resp == 1:
        clear_queue(chat_id)
        await set_loop(chat_id, 0)
        return

    if resp[0] == 2:
        await app.send_message(chat_id, resp[1])
        return

    total_time = int(time.time() - resp[5])
    m = await app.send_message(
        chat_id,
        f"**ѕσηg ιѕ ρℓαуιηg ιη ν¢**\n\n"
        f"**SongName :** [{resp[0][:19]}]({resp[4]})\n"
        f"**Duration :** {resp[1]} **Minutes**\n"
        f"**Response Time :** `{total_time}` **Seconds**\n\n"
        f"[**Click Here For Make Your Own Music Bot**](https://t.me/NotRealAbhiii)",
        disable_web_page_preview=True,
    )
    await asyncio.sleep(60)
    await m.delete()


# ─────────────────────────────
# STOP VC + FULL CLEAN
# ─────────────────────────────
async def stop(chat_id):
    try:
        await call.leave_call(chat_id)
    except:
        pass

    clear_queue(chat_id)
    await set_loop(chat_id, 0)

    if chat_id in seek_chats:
        del seek_chats[chat_id]

    logging.info(f"VC stopped & cleaned | chat_id={chat_id}")


# ─────────────────────────────
# LEFT CALL EVENT (SAFETY)
# ─────────────────────────────
@call.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
async def on_left_call(_: PyTgCalls, update):
    await stop(update.chat_id)
