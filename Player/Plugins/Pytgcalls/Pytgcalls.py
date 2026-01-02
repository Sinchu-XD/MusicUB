"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import time
import asyncio
from pytgcalls import PyTgCalls, filters
from pytgcalls.types import Update, MediaStream, ChatUpdate

from Player import call, app, seek_chats
from Player.Utils.Loop import get_loop, set_loop
from Player.Utils.Queue import (
    QUEUE,
    get_queue,
    pop_an_item,
    clear_queue,
)

# ─────────────────────────────
# INTERNAL SKIP / AUTO-NEXT
# ─────────────────────────────
async def _skip(chat_id):
    loop = await get_loop(chat_id)
    queue = get_queue(chat_id)

    # ───── LOOP ENABLED ─────
    if loop > 0 and queue:
        await set_loop(chat_id, loop - 1)

        title, duration, stream_url, requested_by = queue[0]

        await call.play(
            chat_id,
            MediaStream(stream_url, video_flags=MediaStream.Flags.IGNORE)
        )

        return title, duration, stream_url

    # ───── NORMAL QUEUE ─────
    if not queue:
        await stop(chat_id)
        return None

    if len(queue) == 1:
        clear_queue(chat_id)
        await stop(chat_id)
        return None

    # ───── NEXT SONG ─────
    pop_an_item(chat_id)
    title, duration, stream_url, requested_by = get_queue(chat_id)[0]

    await call.play(
        chat_id,
        MediaStream(stream_url, video_flags=MediaStream.Flags.IGNORE)
    )

    return title, duration, stream_url


# ─────────────────────────────
# STREAM END HANDLER
# ─────────────────────────────
@call.on_update(filters.stream_end())
async def on_stream_end(client: PyTgCalls, update: Update):
    chat_id = update.chat_id
    seek_chats.pop(chat_id, None)

    result = await _skip(chat_id)
    if not result:
        return

    title, duration, stream_url = result

    m = await app.send_message(
        chat_id,
        f"**🎶 Now Playing**\n\n"
        f"**Title:** {title[:25]}\n"
        f"**Duration:** {duration}\n"
        f"[Enjoy the music ❤️]"
    )

    await asyncio.sleep(45)
    await m.delete()


# ─────────────────────────────
# STOP VC
# ─────────────────────────────
async def stop(chat_id):
    try:
        await call.leave_call(chat_id)
    except:
        pass


# ─────────────────────────────
# LEFT VC CLEANUP
# ─────────────────────────────
@call.on_update(filters.chat_update(ChatUpdate.Status.LEFT_CALL))
async def on_left_call(client, update):
    chat_id = update.chat_id
    await stop(chat_id)
    clear_queue(chat_id)
    await set_loop(chat_id, 0)
    seek_chats.pop(chat_id, None)

