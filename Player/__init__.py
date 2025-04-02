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


seek_chats = {}