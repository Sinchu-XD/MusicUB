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

# Notify when a user joins VC
@call.on_participants_change()
async def participant_change_handler(_, chat_id: int, participants: list[GroupCallParticipant]):
    for participant in participants:
        if not participant.is_self:
            user = await app.get_users(participant.user_id)
            await app.send_message(chat_id, f"👤 **{user.first_name} Joined The Voice Chat!**\n\n** ABHISHEK Aapka VC Me Swagat Karta Hai**")

# Function to check VC listeners and leave if empty
async def check_listeners(chat_id):
    await asyncio.sleep(5)  # Delay to prevent false triggers
    participants = await call.get_participants(chat_id)

    # Exclude the bot itself
    listeners = [p for p in participants if not p.is_self]

    if not listeners:
        await app.send_message(chat_id, "**Mujhe Akela Mat Chhodo Guys**\n\n** Mujhe Akele Dar Lagta Hai..**")
        

# Notify when a user leaves VC
@call.on_participant_list_updated()
async def participant_leave_handler(_, chat_id: int, participants: list[GroupCallParticipant]):
    for participant in participants:
        if not participant.is_self:
            user = await app.get_users(participant.user_id)
            await app.send_message(chat_id, f"👋 {user.first_name} ** Aap Mujhe Akela Chhod Ke Mt Jaao Yrr Please**")

    # Check if VC is empty after someone leaves
    await check_listeners(chat_id)
