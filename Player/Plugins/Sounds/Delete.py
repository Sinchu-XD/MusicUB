from Player import app
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio


@app.on_message(filters.command("purgeall") & filters.me)
async def purge_all_messages(client: Client, message: Message):
    chat_id = message.chat.id
    await message.reply("🧹 Purging all messages...")

    async for msg in client.get_chat_history(chat_id):
        try:
            await client.delete_messages(chat_id, msg.id)
        except Exception as e:
            print(f"❌ Failed to delete message {msg.id}: {e}")
        await asyncio.sleep(0.1)  # prevent flood wait

    await client.send_message(chat_id, "✅ All messages deleted!")
