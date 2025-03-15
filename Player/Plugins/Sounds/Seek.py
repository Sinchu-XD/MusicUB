
import asyncio
from pyrogram import filters
from Player import app, call
from pytgcalls.types import MediaStream, AudioQuality


@app.on_message(filters.command("seek"))
async def seek_music(client, message):
    global current_chat
    if current_chat:
        try:
            seconds = int(message.command[1])
            await call.seek_stream(current_chat, seconds)
            await message.reply(f"⏩ Seeked to {seconds} seconds!")
        except Exception as e:
            await message.reply(f"❌ Error: {e}")
    else:
        await message.reply("❌ No song is currently playing!")

@app.on_message(filters.command("rewind"))
async def rewind_music(client, message):
    global current_chat
    if current_chat:
        try:
            seconds = int(message.command[1])
            await call.seek_stream(current_chat, -seconds)
            await message.reply(f"⏪ Rewinded by {seconds} seconds!")
        except Exception as e:
            await message.reply(f"❌ Error: {e}")
    else:
        await message.reply("❌ No song is currently playing!")


### For Read Only
