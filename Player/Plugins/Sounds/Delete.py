from Player import app
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio
from config import OWNER_ID

@app.on_message(filters.command("purgeall") & filters.user(OWNER_ID))
async def purge_all_messages(client: Client, message: Message):
    chat_id = message.chat.id
    try:
        await message.reply("🧹 Purging all messages...")
    except Exception as e:
        print(f"❌ Can't reply: {e}")

    async for msg in client.get_chat_history(chat_id):
        try:
            await client.delete_messages(chat_id, msg.id)
        except Exception as e:
            print(f"❌ Failed to delete message {msg.id}: {e}")
        await asyncio.sleep(0.1)

    try:
        await client.send_message(chat_id, "✅ All messages deleted!")
    except Exception as e:
        print(f"❌ Could not send confirmation: {e}")
