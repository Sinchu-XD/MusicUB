from Player import app
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from config import OWNER_ID

SUDO_USERS = [7862043458, 8091116698]  


@app.on_message(filters.command("purgeall"))
async def purge_all(client: Client, message: Message):
    user_id = message.from_user.id

    # Check if user is authorized
    if user_id != OWNER_ID and user_id not in SUDO_USERS:
        return await message.reply("🚫 **Only Rex Bhadwa And Abhi Randi Use This Command**")

    if len(message.command) < 2:
        return await message.reply("❌ Please give a Chat ID or username.\nUsage: `/purgeall -1001234567890`", quote=True)

    chat_id = message.command[1]

    deleted = 0
    failed = 0
    await message.reply(f"🧹 Starting purge in `{chat_id}`...")

    try:
        async for msg in client.get_chat_history(chat_id):
            try:
                await client.delete_messages(chat_id, msg.id)
                deleted += 1
                await asyncio.sleep(0.05)  # avoid FloodWait
            except Exception as e:
                failed += 1
                print(f"Failed to delete {msg.id} - {e}")
    except Exception as e:
        return await message.reply(f"❌ Error: `{e}`")

    await message.reply(f"✅ Purge complete!\nDeleted: `{deleted}`\nFailed: `{failed}`")
    print(f"✅ Purge from {chat_id} done. Deleted: {deleted}, Failed: {failed}")

    # ✅ Console log with bot username
    me = await client.get_me()
    print(f"✅ Purged {deleted_count} messages from chat {chat_id} as @{me.username}")

print("✅ UserBot started...")
