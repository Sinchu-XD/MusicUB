"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import asyncio
import logging
from pytgcalls import PyTgCalls, filters
from pytgcalls.types import Update, MediaStream, ChatUpdate

from Player import call, app, seek_chats
from Player.Utils.Loop import get_loop, set_loop
from Player.Utils.Queue import (
    get_queue,
    pop_an_item,
    clear_queue,
    add_to_queue,
)
from Player.Utils.AutoPlay import is_autoplay_on, get_recommendation
from Player.Core import Userbot

# 🔑 shared from play.py
from Player.Plugins.Sounds.Play import last_played_title

logging.basicConfig(level=logging.INFO)

# ─────────────────────────────
# INTERNAL NEXT / LOOP / AUTOPLAY
# ─────────────────────────────
async def _next(chat_id):
    loop = await get_loop(chat_id)
    queue = get_queue(chat_id)

    # ───── LOOP ENABLED ─────
    if loop > 0 and queue:
        await set_loop(chat_id, loop - 1)
        title, duration, stream_url, _ = queue[0]
        await call.play(
            chat_id,
            MediaStream(stream_url, video_flags=MediaStream.Flags.IGNORE)
        )
        return title, duration

    # ───── NORMAL QUEUE ─────
    if queue:
        if len(queue) > 1:
            pop_an_item(chat_id)
            title, duration, stream_url, _ = get_queue(chat_id)[0]
            await call.play(
                chat_id,
                MediaStream(stream_url, video_flags=MediaStream.Flags.IGNORE)
            )
            return title, duration

        # last song finished
        clear_queue(chat_id)

    # ───── AUTOPLAY ─────
    if await is_autoplay_on(chat_id):
        last_title = last_played_title.get(chat_id)
        if last_title:
            rec = await get_recommendation(last_title)
            if rec:
                title, duration, stream_url = rec
                add_to_queue(chat_id, title, duration, stream_url, "AutoPlay")
                last_played_title[chat_id] = title

                await call.play(
                    chat_id,
                    MediaStream(stream_url, video_flags=MediaStream.Flags.IGNORE)
                )
                return title, duration

    # ───── NOTHING LEFT ─────
    await hard_cleanup(chat_id)
    return None


# ─────────────────────────────
# STREAM END HANDLER
# ─────────────────────────────
@call.on_update(filters.stream_end())
async def on_stream_end(client: PyTgCalls, update: Update):
    chat_id = update.chat_id
    seek_chats.pop(chat_id, None)

    result = await _next(chat_id)
    if not result:
        return

    title, duration = result
    msg = await app.send_message(
        chat_id,
        f"**🎶 Now Playing**\n\n"
        f"**Title:** {title[:25]}\n"
        f"**Duration:** {duration}"
    )

    await asyncio.sleep(40)
    await msg.delete()


# ─────────────────────────────
# HARD CLEANUP (CORE FIX)
# ─────────────────────────────
async def hard_cleanup(chat_id):
    logging.warning(f"VC cleanup triggered for chat {chat_id}")

    clear_queue(chat_id)
    seek_chats.pop(chat_id, None)
    last_played_title.pop(chat_id, None)
    await set_loop(chat_id, 0)

    try:
        await call.leave_call(chat_id)
    except:
        pass


# ─────────────────────────────
# VC LEFT / DISCONNECTED HANDLER
# ─────────────────────────────
@call.on_update(filters.chat_update(
    ChatUpdate.Status.LEFT_CALL
))
async def on_left_call(client, update):
    await hard_cleanup(update.chat_id)


# ─────────────────────────────
# EXTRA SAFETY: VC KICK / END
# ─────────────────────────────
@call.on_update(filters.chat_update(
    ChatUpdate.Status.KICKED
))
async def on_kicked_call(client, update):
    await hard_cleanup(update.chat_id)
