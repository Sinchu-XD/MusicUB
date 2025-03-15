
import asyncio
from pyrogram import filters
from Player import app, call
from pytgcalls.types import MediaStream, AudioQuality

current_chat = None


@app.on_message(filters.command("seek"))
async def seek_music(client, message):
    chat_id = message.chat.id
    
    if chat_id not in call.active_calls:
        return await message.reply("❌ No song is currently playing!")

    print(call.active_calls)  # Debugging active calls
    
    try:
        await call.seek_stream(chat_id, 30)  # Seek to 30 seconds
        await message.reply("✅ Seeked to 30 seconds!")
    except Exception as e:
        await message.reply(f"❌ Error: {e}")

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
