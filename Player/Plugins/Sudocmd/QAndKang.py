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
import os
import base64
import requests
from pyrofork import Client, filters

# API Endpoint
QUOTLY_API = "https://bot.lyo.su/quote/generate"


@app.on_message(filters.command("q") & filters.reply)
async def quottly(client, message):
    msg = await message.reply_text("⚡ Generating Quote...")
    reply = message.reply_to_message
    sender = reply.from_user
    
    # Prepare Quote Data
    content = {
        "type": "quote",
        "format": "webp",
        "backgroundColor": "#1b1429",
        "width": 512,
        "height": 768,
        "scale": 2,
        "messages": [
            {
                "chatId": reply.chat.id,
                "avatar": True,
                "from": {
                    "id": sender.id,
                    "first_name": sender.first_name or "Deleted Account",
                    "username": sender.username,
                    "language_code": "en"
                },
                "text": reply.text or "",
            }
        ],
    }
    
    try:
        response = requests.post(QUOTLY_API, json=content, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if data.get("ok"):
            file_path = "quote.webp"
            with open(file_path, "wb") as file:
                file.write(base64.b64decode(data["result"]["image"]))
            
            await message.reply_document(file_path, caption="Here's your quote!")
            os.remove(file_path)
        else:
            await msg.edit("❌ Failed to generate a quote!")
    except requests.exceptions.RequestException as e:
        await msg.edit(f"❌ API Error: {str(e)}")
    
    await msg.delete()


# Start UserBot
print("🚀 UserBot is Running!")

