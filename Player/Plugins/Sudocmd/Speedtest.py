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
    
    loop = asyncio.get_event_loop()
    result, download_speed, upload_speed = await loop.run_in_executor(None, testspeed)

    if isinstance(result, str):  # If an error occurred
        return await msg.edit(f"❌ **Speed Test Failed**\nError: `{result}`")

    # Safe extraction of values
    isp = result.get("client", {}).get("isp", "Unknown")
    country = result.get("client", {}).get("country", "Unknown")
    isp_rating = result.get("client", {}).get("isprating", "N/A")

    server_name = result.get("server", {}).get("name", "Unknown")
    server_country = result.get("server", {}).get("country", "Unknown")
    server_cc = result.get("server", {}).get("cc", "")
    server_sponsor = result.get("server", {}).get("sponsor", "Unknown")
    latency = result.get("server", {}).get("latency", "N/A")
    ping = result.get("ping", "N/A")

    share_link = result.get("share", None)

    output = f"""🚀 **Speed Test Results** 🚀

__**Client:**__
🌐 **ISP:** `{isp}`
🌍 **Country:** `{country}`
⭐ **ISP Rating:** `{isp_rating}`

__**Server:**__
🏢 **Name:** `{server_name}`
📌 **Location:** `{server_country}, {server_cc}`
🔰 **Sponsor:** `{server_sponsor}`
⚡ **Latency:** `{latency} ms`
📡 **Ping:** `{ping} ms`

__**Speed:**__
⬇️ **Download:** `{download_speed:.2f} Mbps`
⬆️ **Upload:** `{upload_speed:.2f} Mbps`
"""

    if share_link:
        await app.send_photo(
            chat_id=message.chat.id,
            photo=share_link,
            caption=output
        )
    else:
        await msg.edit(output)

    await msg.delete()
