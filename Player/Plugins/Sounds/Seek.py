import asyncio
from pyrogram import filters
from Player import app, call


@app.on_message(filters.command("seek"))
async def seek_audio(client, message):
    chat_id = message.chat.id
    if len(message.command) < 2:
        await message.reply_text("❌ **Usage:** /seek <seconds>")
        return
    
    try:
        seconds = int(message.command[1])
        await call.seek_stream(chat_id, seconds)
        await message.reply_text(f"⏩ **Seeked to:** {seconds} seconds")
    except Exception as e:
        await message.reply_text(f"❌ **Error:** `{e}`")
