import os
import requests
from pyrogram import Client, filters
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName, InputDocument, InputStickerSetItem
from pyrogram.enums import ChatType
from pyrogram.types import Message
import random
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

    try:
        await message.reply_photo(file_path, caption="✨ Here is your quote!")
    except Exception as e:
        await message.reply_document(file_path, caption="✨ Here is your quote!")
    
    # Cleanup
    os.remove(file_path)
    

    await msg.delete()

# Image URLs
IMAGES = {
    "horny": "https://telegra.ph/file/daad931db960ea40c0fca.gif",
    "gay": "https://telegra.ph/file/a23e9fd851fb6bc771686.gif",
    "lezbian": "https://telegra.ph/file/5609b87f0bd461fc36acb.gif",
    "boob": "https://i.gifer.com/8ZUg.gif",
    "cock": "https://telegra.ph/file/423414459345bf18310f5.gif",
    "cute": "https://64.media.tumblr.com/d701f53eb5681e87a957a547980371d2/tumblr_nbjmdrQyje1qa94xto1_500.gif",
}

# Command Handlers
async def generate_response(message, category, emoji, unit=""):
    """Generates a random response with a percentage and an image."""
    user = message.from_user
    percentage = random.randint(1, 100)
    text = f"**{emoji} {user.mention} is {percentage}% {category}{unit}!**"

    await message.reply_photo(photo=IMAGES[category], caption=text)


@app.on_message(filters.command("horny"))
async def horny_cmd(client, message):
    await generate_response(message, "horny", "🔥")


@app.on_message(filters.command("gay"))
async def gay_cmd(client, message):
    await generate_response(message, "gay", "🍷")


@app.on_message(filters.command("lezbian"))
async def lezbian_cmd(client, message):
    await generate_response(message, "lezbian", "💜")


@app.on_message(filters.command("boob"))
async def boob_cmd(client, message):
    await generate_response(message, "boob", "🍒", " boob size")


@app.on_message(filters.command("cock"))
async def cock_cmd(client, message):
    await generate_response(message, "cock", "🍆", "cm")


@app.on_message(filters.command("cute"))
async def cute_cmd(client, message):
    await generate_response(message, "cute", "🍑")


# Start UserBot
print("🚀 UserBot is Running!")

