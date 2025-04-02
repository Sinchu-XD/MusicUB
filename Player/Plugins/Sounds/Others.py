"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter
import asyncio
from Player import app
from Player.Utils.Queue import clear_queue
from Player.Utils.Loop import get_loop, set_loop
from Player.Core import Userbot
from Player.Misc import SUDOERS
from Player.Utils.Delete import delete_messages
import config

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX

STOP_COMMAND = ["STOP", "CHUP"]
PAUSE_COMMAND = ["PAUSE"]
RESUME_COMMAND = ["RESUME"]
MUTE_COMMAND = ["MUTE"]
UNMUTE_COMMAND = ["UNMUTE"]
VOLUME_COMMAND = ["VOL", "VOLUME"]
LOOP_COMMAND = ["LOOP"]
LOOPEND_COMMAND = ["ENDLOOP"]

@app.on_message(filters.command(STOP_COMMAND, PREFIX))
async def _stop(_, message):
    administrators = [
        admin.user.id async for admin in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS)
    ]
    if message.from_user.id in SUDOERS or message.from_user.id in administrators:
        Text = await Userbot.stop(message.chat.id)
        clear_queue(message.chat.id)
        m = await message.reply_text(Text)
    else:
        m = await message.reply_text("Abe saale... terepe perms naa hai admins ko bol...")
    asyncio.create_task(delete_messages(message, m))

@app.on_message(filters.command(PAUSE_COMMAND, PREFIX))
async def _pause(_, message):
    administrators = [
        admin.user.id async for admin in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS)
    ]
    if message.from_user.id in SUDOERS or message.from_user.id in administrators:
        Text = await Userbot.pause(message.chat.id)
        m = await message.reply_text(Text)
    else:
        m = await message.reply_text("Abe saale... terepe perms naa hai admins ko bol...")
    asyncio.create_task(delete_messages(message, m))

@app.on_message(filters.command(RESUME_COMMAND, PREFIX))
async def _resume(_, message):
    administrators = [
        admin.user.id async for admin in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS)
    ]
    if message.from_user.id in SUDOERS or message.from_user.id in administrators:
        Text = await Userbot.resume(message.chat.id)
        m = await message.reply_text(Text)
    else:
        m = await message.reply_text("Abe saale... terepe perms naa hai admins ko bol...")
    asyncio.create_task(delete_messages(message, m))

@app.on_message(filters.command(MUTE_COMMAND, PREFIX))
async def _mute(_, message):
    Text = await Userbot.mute(message.chat.id)
    m = await message.reply_text(Text)
    asyncio.create_task(delete_messages(message, m))

@app.on_message(filters.command(UNMUTE_COMMAND, PREFIX))
async def _unmute(_, message):
    Text = await Userbot.unmute(message.chat.id)
    m = await message.reply_text(Text)
    asyncio.create_task(delete_messages(message, m))

@app.on_message(filters.command(VOLUME_COMMAND, PREFIX))
async def _volume(_, message):
    try:
        vol = int(message.text.split()[1])
        Text = await Userbot.changeVolume(message.chat.id, vol)
    except:
        Text = await Userbot.changeVolume(message.chat.id)
    m = await message.reply_text(Text)
    asyncio.create_task(delete_messages(message, m))

@app.on_message(filters.command(LOOP_COMMAND, PREFIX))
async def _loop(_, message):
    administrators = [
        admin.user.id async for admin in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS)
    ]
    if message.from_user.id in SUDOERS or message.from_user.id in administrators:
        loop = await get_loop(message.chat.id)
        if loop == 0:
            await set_loop(message.chat.id, 5)
            m = await message.reply_text("Loop enabled. Now current song will be played 5 times")
        else:
            m = await message.reply_text("Loop already enabled")
    else:
        m = await message.reply_text("Abe saale... terepe perms naa hai admins ko bol...")
    asyncio.create_task(delete_messages(message, m))

@app.on_message(filters.command(LOOPEND_COMMAND, PREFIX))
async def _endLoop(_, message):
    administrators = [
        admin.user.id async for admin in app.get_chat_members(message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS)
    ]
    if message.from_user.id in SUDOERS or message.from_user.id in administrators:
        loop = await get_loop(message.chat.id)
        if loop == 0:
            m = await message.reply_text("Loop is not enabled")
        else:
            await set_loop(message.chat.id, 0)
            m = await message.reply_text("Loop Disabled")
    else:
        m = await message.reply_text("Abe saale... terepe perms naa hai admins ko bol...")
    asyncio.create_task(delete_messages(message, m))
