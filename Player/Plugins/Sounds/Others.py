"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import asyncio
import config

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter

from Player import app
from Player.Core import Userbot
from Player.Misc import SUDOERS
from Player.Utils.Queue import clear_queue
from Player.Utils.Loop import get_loop, set_loop
from Player.Utils.Delete import delete_messages

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX

STOP_COMMAND = ["END", "CHUP"]
PAUSE_COMMAND = ["PAUSE"]
RESUME_COMMAND = ["RESUME"]
MUTE_COMMAND = ["MUTE"]
UNMUTE_COMMAND = ["UNMUTE"]
LOOP_COMMAND = ["LOOP"]
LOOPEND_COMMAND = ["ENDLOOP"]


# ─────────────────────────────
# ADMIN CHECK
# ─────────────────────────────
async def is_admin(chat_id, user_id):
    if user_id in SUDOERS:
        return True

    admins = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]
    return user_id in admins


# ─────────────────────────────
# STOP
# ─────────────────────────────
@app.on_message(filters.command(STOP_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def stop_music(_, message):
    if not await is_admin(message.chat.id, message.from_user.id):
        m = await message.reply_text("❌ **Only admins can stop music.**")
        return asyncio.create_task(delete_messages(message, m))

    text = await Userbot.stop(message.chat.id)
    clear_queue(message.chat.id)

    m = await message.reply_text(text)
    asyncio.create_task(delete_messages(message, m))


# ─────────────────────────────
# PAUSE
# ─────────────────────────────
@app.on_message(filters.command(PAUSE_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def pause_music(_, message):
    if not await is_admin(message.chat.id, message.from_user.id):
        m = await message.reply_text("❌ **Only admins can pause music.**")
        return asyncio.create_task(delete_messages(message, m))

    text = await Userbot.pause(message.chat.id)
    m = await message.reply_text(text)
    asyncio.create_task(delete_messages(message, m))


# ─────────────────────────────
# RESUME
# ─────────────────────────────
@app.on_message(filters.command(RESUME_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def resume_music(_, message):
    if not await is_admin(message.chat.id, message.from_user.id):
        m = await message.reply_text("❌ **Only admins can resume music.**")
        return asyncio.create_task(delete_messages(message, m))

    text = await Userbot.resume(message.chat.id)
    m = await message.reply_text(text)
    asyncio.create_task(delete_messages(message, m))


# ─────────────────────────────
# MUTE
# ─────────────────────────────
@app.on_message(filters.command(MUTE_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def mute_music(_, message):
    text = await Userbot.mute(message.chat.id)
    m = await message.reply_text(text)
    asyncio.create_task(delete_messages(message, m))


# ─────────────────────────────
# UNMUTE
# ─────────────────────────────
@app.on_message(filters.command(UNMUTE_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def unmute_music(_, message):
    text = await Userbot.unmute(message.chat.id)
    m = await message.reply_text(text)
    asyncio.create_task(delete_messages(message, m))


# ─────────────────────────────
# LOOP
# ─────────────────────────────
@app.on_message(filters.command(LOOP_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def loop_music(_, message):
    if not await is_admin(message.chat.id, message.from_user.id):
        m = await message.reply_text("❌ **Only admins can set loop.**")
        return asyncio.create_task(delete_messages(message, m))

    try:
        count = int(message.text.split()[1])
        if count < 1:
            raise ValueError
    except (IndexError, ValueError):
        m = await message.reply_text(
            "**Usage:** `/loop <count>`\n"
            "➤ Example: `/loop 3`\n"
            "➤ Minimum: 1"
        )
        return asyncio.create_task(delete_messages(message, m))

    await set_loop(message.chat.id, count)
    m = await message.reply_text(f"🔁 **Loop enabled for {count} times.**")
    asyncio.create_task(delete_messages(message, m))


# ─────────────────────────────
# END LOOP
# ─────────────────────────────
@app.on_message(filters.command(LOOPEND_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def end_loop_music(_, message):
    if not await is_admin(message.chat.id, message.from_user.id):
        m = await message.reply_text("❌ **Only admins can disable loop.**")
        return asyncio.create_task(delete_messages(message, m))

    loop = await get_loop(message.chat.id)
    if loop == 0:
        m = await message.reply_text("ℹ️ **Loop is not enabled.**")
    else:
        await set_loop(message.chat.id, 0)
        m = await message.reply_text("✅ **Loop disabled.**")

    asyncio.create_task(delete_messages(message, m))
