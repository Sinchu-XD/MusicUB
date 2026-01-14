"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import logging
import time
import asyncio
import config

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter

from Player import app, call, seek_chats
from Player.Core import Userbot
from Player.Misc import SUDOERS
from Player.Utils.Loop import get_loop, set_loop
from Player.Utils.Delete import delete_messages
from Player.Utils.Queue import (
    get_queue,
    pop_an_item,
    clear_queue,
    add_to_queue,
)
from Player.Utils.AutoPlay import is_autoplay_on, get_recommendation
from Player.Plugins.Sounds.Play import last_played_title

logging.basicConfig(level=logging.INFO)

SKIP_COMMAND = ["SKIP"]
QUEUE_COMMAND = ["QUEUE"]

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


# ─────────────────────────────
# STOP VC + FULL CLEAN 🔥
# ─────────────────────────────
async def stop(chat_id: int):
    try:
        await call.leave_call(chat_id)
    except Exception:
        pass

    clear_queue(chat_id)
    await set_loop(chat_id, 0)

    if chat_id in seek_chats:
        del seek_chats[chat_id]

    logging.info(f"VC stopped & cleaned | chat_id={chat_id}")


# ─────────────────────────────
# CHECK VC ACTIVE
# ─────────────────────────────
def is_vc_active(chat_id: int) -> bool:
    try:
        return call.is_connected(chat_id)
    except Exception:
        return False


# ─────────────────────────────
# SKIP COMMAND
# ─────────────────────────────
@app.on_message(filters.command(SKIP_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def skip_song(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    mention = message.from_user.mention

    seek_chats.pop(chat_id, None)

    # ❌ VC not running
    if not is_vc_active(chat_id):
        clear_queue(chat_id)
        return await message.reply_text("❌ **Nothing is playing in VC.**")

    admins = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]

    if message.from_user.id not in admins and message.from_user.id not in SUDOERS:
        return await message.reply_text(
            "❌ **You don't have permission to skip songs.**"
        )

    m = await message.reply_text(f"⏩ **Skipping song...**\n🎤 {mention}")

    # ───── LOOP CHECK ─────
    if await get_loop(chat_id) != 0:
        await m.edit(
            f"🔄 **Loop is enabled!** Disable it with `{PREFIX}endloop`."
        )
        return await delete_messages(message, m)

    queue = get_queue(chat_id)

    # ───── NO / LAST SONG ─────
    if not queue or len(queue) == 1:
        clear_queue(chat_id)

        # ─── AUTOPLAY ───
        if await is_autoplay_on(chat_id):
            last_title = last_played_title.get(chat_id)
            if last_title:
                rec = await get_recommendation(last_title)
                if rec:
                    title, duration, stream_url = rec

                    add_to_queue(
                        chat_id,
                        title,
                        duration,
                        stream_url,
                        "AutoPlay",
                    )
                    last_played_title[chat_id] = title

                    status, text = await Userbot.playAudio(chat_id, stream_url)
                    if not status:
                        return await m.edit(text)

                    total_time = int(time.time() - start_time)
                    await m.edit(
                        f"**🎶 Now Playing (AutoPlay)**\n\n"
                        f"**Title:** {title[:25]}\n"
                        f"**Duration:** {duration}\n"
                        f"**Response:** {total_time}s"
                    )
                    return await delete_messages(message, m)

        # autoplay off → stop VC
        await stop(chat_id)
        await m.edit(
            f"🚫 **Queue is empty.** Leaving VC...\n🎤 {mention}"
        )
        return await delete_messages(message, m)

    # ───── REMOVE CURRENT ─────
    pop_an_item(chat_id)

    # ───── PLAY NEXT ─────
    title, duration, stream_url, requested_by = get_queue(chat_id)[0]
    last_played_title[chat_id] = title

    try:
        status, text = await Userbot.playAudio(chat_id, stream_url)
        if not status:
            return await m.edit(text)
    except Exception as e:
        logging.error(f"Error playing next song: {e}")
        return await m.edit("❌ Failed to play next song.")

    total_time = int(time.time() - start_time)

    await m.edit(
        f"**🎶 Now Playing**\n\n"
        f"**Title:** {title[:25]}\n"
        f"**Duration:** {duration}\n"
        f"**Requested by:** {requested_by}\n"
        f"**Response:** {total_time}s"
    )
    return await delete_messages(message, m)


# ─────────────────────────────
# QUEUE COMMAND
# ─────────────────────────────
@app.on_message(filters.command(QUEUE_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def show_queue(_, message):
    chat_id = message.chat.id
    queue = get_queue(chat_id)

    if not queue:
        return await message.reply_text("📭 **Queue is empty.**")

    output = "**🎶 Now Playing:**\n"
    title, duration, _, requested_by = queue[0]
    output += f"▶️ **{title}** ({duration}) — {requested_by}\n"

    if len(queue) > 1:
        output += "\n**📜 Up Next:**\n"
        for i, item in enumerate(queue[1:], start=1):
            title, duration, _, requested_by = item
            output += f"{i}. {title} ({duration}) — {requested_by}\n"

    await message.reply_text(output)
    
