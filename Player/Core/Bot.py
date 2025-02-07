"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""


from pyrogram import Client
from pytgcalls import PyTgCalls

import config
from ..logging import LOGGER

api_id: int = config.API_ID
api_hash: str = config.API_HASH
session_string: str = config.SESSION_STRING

MusicBot = Client(
    name="Player", api_id=api_id, api_hash=api_hash, session_string=session_string
)

MusicUser = PyTgCalls(MusicBot)
