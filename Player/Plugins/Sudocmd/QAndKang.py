import os
import requests
from pyrogram import Client, filters
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName, InputDocument, InputStickerSetItem
from pyrogram.enums import ChatType
from pyrogram.types import Message

from Player import app


STICKER_PACK_NAME = "LookAbhi"
STICKER_PACK_TITLE = "LookAbhi Stickers"


# 🔹 Kang Command - Steal Stickers & Add to User's Pack
@app.on_message(filters.command("kang") & (filters.group | filters.private))
async def kang_sticker(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("❌ Reply to a sticker to kang it!")

    sticker = message.reply_to_message.sticker
    file_path = await client.download_media(sticker.file_id)
    sticker_emoji = sticker.emoji if sticker.emoji else "🔥"

    user = await client.get_me()
    pack_name = f"{STICKER_PACK_NAME}_{user.id}"  # Unique pack name for each user

    try:
        # Check if the sticker pack exists
        await client.invoke(GetStickerSet(stickerset=InputStickerSetShortName(pack_name)))
        pack_exists = True
    except Exception:
        pack_exists = False

    if pack_exists:
        # Add sticker to existing pack
        await client.add_sticker_to_set(
            user_id=user.id,
            name=pack_name,
            png_sticker=file_path,
            emojis=sticker_emoji
        )
        await message.reply_text(f"✅ Sticker Added! [View Pack](https://t.me/addstickers/{pack_name})")
    else:
        # Create a new sticker pack
        await client.create_sticker_set(
            user_id=user.id,
            name=pack_name,
            title=STICKER_PACK_TITLE,
            png_sticker=file_path,
            emojis=sticker_emoji
        )
        await message.reply_text(f"✅ New Sticker Pack Created! [Click Here](https://t.me/addstickers/{pack_name})")

    os.remove(file_path)  # Cleanup temp file



# 🔹 Quotly Command - Generate Stylish Quotes
import base64
import json
import os
from asyncio import sleep
from random import choice
import aiohttp

# API Endpoint
API_URL = "https://bot.lyo.su/quote/generate"


async def fetch_quote(content):
    """Fetch the quote image from API"""
    async with aiohttp.ClientSession() as session:
        async with session.post(API_URL, json=content) as resp:
            data = await resp.json()
            if data.get("ok"):
                image_data = base64.b64decode(data["result"]["image"])
                file_path = "quote.webp"
                with open(file_path, "wb") as f:
                    f.write(image_data)
                return file_path
            return None

@app.on_message(filters.command("q") & filters.reply)
async def quote_message(client, message):
    """Handle /q command to generate a quote"""
    reply = message.reply_to_message

    if not reply:
        return await message.reply_text("❌ Please reply to a message to create a quote!")

    msg = await message.reply_text("⏳ Generating quote...")

    user = reply.from_user
    content = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": "#1b1429",
        "width": 512,
        "height": 768,
        "scale": 2,
        "messages": [
            {
                "entities": [],
                "chatId": reply.chat.id,
                "avatar": True,
                "from": {
                    "id": user.id,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "username": user.username,
                    "language_code": "en",
                    "title": user.first_name,
                    "name": f"{user.first_name} {user.last_name or ''}".strip(),
                    "type": "private",
                },
                "text": reply.text or "🖼 Media Message",
            }
        ],
    }

    file_path = await fetch_quote(content)

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
    converted_file = file_path.replace(".webp", ".png")
    Image.open(file_path).save(converted_file, "PNG")
    await message.reply_photo(converted_file, caption="✨ Here is your quote!")
    os.remove(file_path)
    os.remove(converted_file)
else:
    await message.reply_text("❌ Quote generation failed. Please try again.")

    await msg.delete()


# Start UserBot
print("🚀 UserBot is Running!")

