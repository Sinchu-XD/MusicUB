import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message, InputStickerSet, InputSticker
from Player import app


STICKER_PACK_NAME = "LookAbhi"
STICKER_PACK_TITLE = "LookAbhi Stickers"


# 🔹 Kang Command - Steal Stickers & Add to User's Pack
@app.on_message(filters.command("kang") & filters.me)
async def kang_sticker(client: Client, message: Message):
    if not message.reply_to_message or not message.reply_to_message.sticker:
        return await message.reply_text("❌ Reply to a sticker to kang it!")

    sticker = message.reply_to_message.sticker
    file_path = await client.download_media(sticker.file_id)
    sticker_emoji = sticker.emoji if sticker.emoji else "🔥"

    user = await client.get_me()
    pack_name = f"LookAbhi_{user.id}"

    # Check if sticker pack exists
    existing_packs = await client.invoke("stickers.getStickerSet", name=pack_name)
    if not existing_packs:
        # Create a new sticker pack
        await client.invoke(
            "stickers.createStickerSet",
            user_id=user.id,
            title=STICKER_PACK_TITLE,
            name=pack_name,
            stickers=[InputSticker(sticker=file_path, emoji=sticker_emoji)]
        )
        await message.reply_text(f"✅ New Sticker Pack Created! [Click Here](https://t.me/addstickers/{pack_name})")
    else:
        # Add sticker to existing pack
        await client.invoke(
            "stickers.addStickerToSet",
            user_id=user.id,
            name=pack_name,
            sticker=InputSticker(sticker=file_path, emoji=sticker_emoji)
        )
        await message.reply_text(f"✅ Sticker Added! [View Pack](https://t.me/addstickers/{pack_name})")

    os.remove(file_path)

# 🔹 Quotly Command - Generate Stylish Quotes
@app.on_message(filters.command("quote") & filters.me)
async def quotly(client: Client, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("❌ Reply to a message to create a quote!")

    msg_text = message.reply_to_message.text or message.reply_to_message.caption

    if not msg_text:
        return await message.reply_text("❌ Cannot quote an empty message!")

    url = "https://api.quotly.xyz/generate"
    data = {"quote": msg_text, "author": message.reply_to_message.from_user.first_name}
    
    response = requests.post(url, json=data)

    if response.status_code == 200:
        await message.reply_photo(response.content)
    else:
        await message.reply_text("❌ Failed to generate a quote!")

# Start UserBot
print("🚀 UserBot is Running!")
app.run()
