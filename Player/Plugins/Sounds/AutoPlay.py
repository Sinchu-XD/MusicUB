"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from pyrogram import filters
from pyrogram.enums import ChatMembersFilter

from Player import app
from Player.Misc import SUDOERS
from Player.Utils.AutoPlay import autoplay, is_autoplay_on
import config

AUTOPLAY_COMMAND = ["AP", "AUTOPLAY"]

PREFIX = config.PREFIX
RPREFIX = config.RPREFIX


# ─────────────────────────────
# AUTOPLAY TOGGLE
# ─────────────────────────────
@app.on_message(filters.command(AUTOPLAY_COMMAND, [PREFIX, RPREFIX]) & filters.group)
async def toggle_autoplay(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id

    # ───── ADMIN CHECK ─────
    admins = [
        admin.user.id
        async for admin in app.get_chat_members(
            chat_id, filter=ChatMembersFilter.ADMINISTRATORS
        )
    ]

    if user_id not in admins and user_id not in SUDOERS:
        return await app.send_message(
            chat_id,
            "❌ **You don't have permission to set Autoplay.**"
        )

    # ───── TOGGLE AUTOPLAY ─────
    status = await autoplay(chat_id)

    if status:
        await app.send_message(
            chat_id,
            "▶️ **AUTOPLAY ENABLED**\n\n"
            "🎧 When queue is empty, similar songs will play automatically."
        )
    else:
        await app.send_message(
            chat_id,
            "⏹️ **AUTOPLAY DISABLED**\n\n"
            "🛑 Bot will leave VC when queue ends."
        )
