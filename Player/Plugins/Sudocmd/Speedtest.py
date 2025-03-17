"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""


from Player.Misc import SUDOERS
from Player import app

from pyrogram import filters
import speedtest
import asyncio


import config

PREFIX = config.PREFIX

RPREFIX = config.RPREFIX

SPEEDTEST_COMMAND = ["speedtest", "speed"]


async def testspeed():
    try:
        test = speedtest.Speedtest()
        test.get_best_server()
        download_speed = test.download() / 1024 / 1024  # Convert to Mbps
        upload_speed = test.upload() / 1024 / 1024  # Convert to Mbps
        test.results.share()
        result = test.results.dict()
        return result, download_speed, upload_speed
    except Exception as e:
        return str(e), None, None

# 		Send Speed of Internet


@app.on_message(
    (
        filters.command(SPEEDTEST_COMMAND, PREFIX)
        | filters.command(SPEEDTEST_COMMAND, RPREFIX)
    )
    & SUDOERS
)
async def speedtest_function(client, message):
    msg = await message.reply_text("⚡ Running speed test, please wait...")

    # ✅ Directly await `testspeed()`
    result, download_speed, upload_speed = await testspeed()

    if isinstance(result, str):  # If an error occurred
        return await msg.edit(f"❌ **Speed Test Failed**\nError: `{result}`")

    output = f"""🚀 **Speed Test Results** 🚀

🌐 **ISP:** `{result['client'].get('isp', 'Unknown')}`
🌍 **Country:** `{result['client'].get('country', 'Unknown')}`
⭐ **ISP Rating:** `{result['client'].get('isprating', 'N/A')}`

🏢 **Server:** `{result['server'].get('name', 'Unknown')}`
📌 **Location:** `{result['server'].get('country', 'Unknown')}, {result['server'].get('cc', '')}`
🔰 **Sponsor:** `{result['server'].get('sponsor', 'Unknown')}`
⚡ **Latency:** `{result['server'].get('latency', 'N/A')} ms`
📡 **Ping:** `{result.get('ping', 'N/A')} ms`

⬇️ **Download:** `{download_speed:.2f} Mbps`
⬆️ **Upload:** `{upload_speed:.2f} Mbps`
"""

    share_link = result.get("share", None)

    if share_link:
        await app.send_photo(chat_id=message.chat.id, photo=share_link, caption=output)
    else:
        await msg.edit(output)

    await msg.delete()
