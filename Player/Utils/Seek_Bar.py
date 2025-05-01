import asyncio
import time
from Player import app

async def update_seek_bar(chat_id, song_duration, start_time, title, ytlink, channel, views):
    progress = 0
    while progress < song_duration:
        current_time = time.time() - start_time
        progress = int((current_time / song_duration) * 100)
        seek_bar = "🟩" * (progress // 2) + "🔲" * (50 - (progress // 2))
        remaining_time = int(song_duration - current_time)
        minutes = remaining_time // 60
        seconds = remaining_time % 60
        time_remaining = f"{minutes:02}:{seconds:02}"

        m = await app.send_message(
            chat_id,
            f"🎶 **Now Playing**\n\n"
            f"🟩 *{seek_bar}* 🔲\n\n"
            f"**Song**: [{title[:30]}]({ytlink})\n"
            f"**Duration**: {minutes}:{seconds} **Minutes**\n"
            f"**Channel**: {channel}\n"
            f"**Views**: {views}\n"
            f"**Time Remaining**: {time_remaining} ⏳",
            disable_web_page_preview=True,
        )

        await asyncio.sleep(1)
        await m.delete()

        if current_time >= song_duration:
            break

def parse_duration(duration_str):
    try:
        parts = list(map(int, duration_str.split(":")))
        if len(parts) == 3:
            return parts[0] * 3600 + parts[1] * 60 + parts[2]
        elif len(parts) == 2:
            return parts[0] * 60 + parts[1]
        elif len(parts) == 1:
            return parts[0]
        else:
            return 0
    except:
        return 0
        
