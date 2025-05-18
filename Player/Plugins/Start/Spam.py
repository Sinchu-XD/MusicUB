import time
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from Player import app
from Player.Utils.Delete import delete_messages

COMMAND_COOLDOWN = 3
user_last_command = {}
enabled_chats = set()

def spam_check():
    return filters.create(func=check_spam)

async def check_spam(_, __, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    if chat_id not in enabled_chats:
        return True
    now = time.time()
    last_time = user_last_command.get((chat_id, user_id), 0)
    if now - last_time < COMMAND_COOLDOWN:
        await message.reply_text("🚫 You're sending commands too fast. Please wait a moment.")
        return False
    user_last_command[(chat_id, user_id)] = now
    return True

@app.on_message(filters.command("spam_on") & filters.group)
async def enable_spam_protection(_, message: Message):
    chat_id = message.chat.id
    enabled_chats.add(chat_id)
    m = await message.reply_text("✅ Spam protection has been enabled in this group.")
    asyncio.create_task(delete_messages(message, m))

@app.on_message(filters.command("spam_off") & filters.group)
async def disable_spam_protection(_, message: Message):
    chat_id = message.chat.id
    enabled_chats.discard(chat_id)
    m = await message.reply_text("❎ Spam protection has been disabled in this group.")
    asyncio.create_task(delete_messages(message, m))
