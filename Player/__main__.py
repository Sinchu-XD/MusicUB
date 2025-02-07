"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import importlib
import asyncio
from pytgcalls import idle

from YMusic import LOGGER
from YMusic.plugins import ALL_MODULES
from YMusic import app, call

loop = asyncio.get_event_loop()


async def init():

    await app.start()
    LOGGER("Player").info("Account Started Successfully")

    for all_module in ALL_MODULES:
        importlib.import_module("YMusic.plugins" + all_module)

    LOGGER("YMusic.plugins").info("Successfully Imported Modules")
    await call.start()
    await idle()


if __name__ == "__main__":
    loop.run_until_complete(init())
    LOGGER("Player").info("Stopping Music Bot! GoodBye")


