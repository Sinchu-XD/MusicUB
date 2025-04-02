import asyncio

async def delete_messages(message=None, m=None, delay_msg=1, delay_reply=10):
    await asyncio.sleep(delay_msg)
    if message:
        try:
            await message.delete()
        except Exception:
            pass  # Ignore if message is already deleted or not found
    await asyncio.sleep(delay_reply - delay_msg)
    if m:
        try:
            await m.delete()
        except Exception:
            pass  # Ignore if reply message is already deleted or not found
