"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import importlib
import asyncio
from pytgcalls import idle

from Player import LOGGER
from Player.Plugins import ALL_MODULES
from Player import app, call


async def init():
    await app.start()
    LOGGER("Player").info("Account Started Successfully")

    for all_module in ALL_MODULES:
        importlib.import_module("Player.Plugins" + all_module)

    LOGGER("Player.Plugins").info("Successfully Imported Modules")
    await call.start()
    await idle()


if __name__ == "__main__":
    try:
        asyncio.run(init())  # ✅ This avoids event loop conflicts
    except KeyboardInterrupt:
        LOGGER("Player").info("Stopping Music Bot! GoodBye")
