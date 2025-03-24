"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import asyncio
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import GroupCallParticipant

from Player.Core.Bot import MusicBot, MusicUser
from .logging import LOGGER
from Player.Misc import sudo

sudo()

app = MusicBot
call = MusicUser

participants_cache = {}

async def check_participants(chat_id):
    """Check for user join/leave events in VC."""
    global participants_cache

    while True:
        await asyncio.sleep(5)  # Check every 5 seconds
        participants = await call.get_participants(chat_id)

        # Exclude bot itself
        listeners = [p for p in participants if not p.is_self]
        count = len(listeners)

        if chat_id not in participants_cache:
            participants_cache[chat_id] = count

        if count > participants_cache[chat_id]:  # Someone joined
            await app.send_message(chat_id, "✅ Someone joined the VC!")

        elif count < participants_cache[chat_id]:  # Someone left
            await app.send_message(chat_id, "⚠️ Someone left the VC!")

        participants_cache[chat_id] = count  # Update cache

        if count == 0:  # No one left in VC
            await app.send_message(chat_id, "⚠️ No one is in VC! Leaving...")
            await call.leave_group_call(chat_id)
            break  # Stop checking for this chat

# Start participant monitoring when a call starts
@call.on_stream_start()
async def on_start(client: Client, chat_id: int):
    asyncio.create_task(check_participants(chat_id))
