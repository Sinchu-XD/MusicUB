"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""


loop = {}


async def get_loop(chat_id: int) -> int:
    lop = loop.get(chat_id)
    if not lop:
        return 0
    return lop


async def set_loop(chat_id: int, mode: int):
    if mode == 0 and chat_id in loop:
        del loop[chat_id]
    loop[chat_id] = mode
