"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""


from pyrogram import filters
from Player import app
from Player.Misc import _boot_
from Player.Utils.Formaters import get_readable_time
import config
import time

PING_COMMAND = ["alive", "ping"]
PREFIX = config.PREFIX


@app.on_message(filters.command(PING_COMMAND, PREFIX))
async def _ping(_, message):
    uptime = get_readable_time(int(time.time() - _boot_))
    await message.reply_text(f"Jinda hu saale...since {uptime}")
