"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""


from pyrogram import filters
from pyrogram.enums import ChatMembersFilter

from Player import app
from Player.Utils.Queue import clear_queue
from Player.Utils.Loop import get_loop, set_loop
from Player.Core import Userbot
from Player.Misc import SUDOERS
import config


PREFIX = config.PREFIX

RPREFIX = config.RPREFIX

STOP_COMMAND = ["END", "CHUP"]

PAUSE_COMMAND = ["PAUSE"]

RESUME_COMMAND = ["RESUME"]

MUTE_COMMAND = ["MUTE"]

UNMUTE_COMMAND = ["UNMUTE"]

VOLUME_COMMAND = ["VOL", "VOLUME"]

LOOP_COMMAND = ["LOOP"]

LOOPEND_COMMAND = ["ENDLOOP"]


@app.on_message(filters.command(STOP_COMMAND, PREFIX))
async def _stop(_, message):
    # Get administrators
    administrators = []
    async for m in app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)
    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
        Text = await Userbot.stop(message.chat.id)
        try:
            clear_queue(message.chat.id)
        except:
            pass
        await message.reply_text(Text)
    else:
        return await message.reply_text(
            "Abe saale... (Maaf karna wo gusse me thora sa idhar udhar ho jata hu) terepe perms naa hai admins ko bol..."
        )


@app.on_message(filters.command(STOP_COMMAND, RPREFIX))
async def _stop(_, message):
    if (len(message.command)) != 2:
        await message.reply_text("You forgot to pass an argument")
    else:
        msg_id = message.text.split(" ", 1)[1]
        Text = await Userbot.stop(msg_id)
        await message.reply_text(Text)


@app.on_message(filters.command(PAUSE_COMMAND, PREFIX))
async def _pause(_, message):
    # Get administrators
    administrators = []
    async for m in app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)
    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
        Text = await Userbot.pause(message.chat.id)
        await message.reply_text(Text)
    else:
        return await message.reply_text(
            "Abe saale... (Maaf karna wo gusse me thora sa idhar udhar ho jata hu) terepe perms naa hai admins ko bol..."
        )


@app.on_message(filters.command(PAUSE_COMMAND, RPREFIX))
async def _pause(_, message):
    if (len(message.command)) != 2:
        await message.reply_text("You forgot to pass an argument")
    else:
        msg_id = message.text.split(" ", 1)[1]
        Text = await Userbot.pause(msg_id)
        await message.reply_text(Text)


@app.on_message(filters.command(RESUME_COMMAND, PREFIX))
async def _resume(_, message):
    # Get administrators
    administrators = []
    async for m in app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)
    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
        Text = await Userbot.resume(message.chat.id)
        await message.reply_text(Text)
    else:
        return await message.reply_text(
            "Abe saale... (Maaf karna wo gusse me thora sa idhar udhar ho jata hu) terepe perms naa hai admins ko bol..."
        )


@app.on_message(filters.command(RESUME_COMMAND, RPREFIX))
async def _resume(_, message):
    if (len(message.command)) != 2:
        await message.reply_text("You forgot to pass an argument")
    else:
        msg_id = message.text.split(" ", 1)[1]
        Text = await Userbot.resume(msg_id)
        await message.reply_text(Text)


@app.on_message(filters.command(MUTE_COMMAND, PREFIX))
async def _mute(_, message):
    if message.from_user and message.from_user.is_self:
        reply = message.edit
    else:
        reply = message.reply_text
    Text = await Userbot.mute(message.chat.id)
    await reply(Text)


@app.on_message(filters.command(MUTE_COMMAND, RPREFIX))
async def _mute(_, message):
    if (len(message.command)) != 2:
        await message.reply_text("You forgot to pass an argument")
    else:
        msg_id = message.text.split(" ", 1)[1]
        Text = await Userbot.mute(msg_id)
        await message.reply_text(Text)


@app.on_message(filters.command(UNMUTE_COMMAND, PREFIX))
async def _unmute(_, message):
    Text = await Userbot.unmute(message.chat.id)
    await message.reply_text(Text)


@app.on_message(filters.command(UNMUTE_COMMAND, RPREFIX))
async def _unmute(_, message):
    if (len(message.command)) != 2:
        await message.reply_text("You forgot to pass an argument")
    else:
        msg_id = message.text.split(" ", 1)[1]
        Text = await Userbot.unmute(msg_id)
        await message.reply_text(Text)


@app.on_message(filters.command(VOLUME_COMMAND, PREFIX))
async def _volume(_, message):
    try:
        vol = int(message.text.split()[1])
        Text = await Userbot.changeVolume(message.chat.id, vol)
    except:
        Text = await Userbot.changeVolume(message.chat.id)
    await message.reply_text(Text)


@app.on_message(filters.command(LOOP_COMMAND, PREFIX))
async def _loop(_, message):
    # Get administrators
    administrators = []
    async for m in app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)
    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
        loop = await get_loop(message.chat.id)
        if loop == 0:
            try:
                await set_loop(message.chat.id, 5)
                await message.reply_text(
                    "Loop enabled. Now current song will be played 5 times"
                )
            except Exception as e:
                return await message.reply_text(f"Error:- <code>{e}</code>")

        else:
            await message.reply_text("Loop already enabled")
    else:
        return await message.reply_text(
            "Abe saale... (Maaf karna wo gusse me thora sa idhar udhar ho jata hu) terepe perms naa hai admins ko bol..."
        )


@app.on_message(filters.command(LOOPEND_COMMAND, PREFIX))
async def _endLoop(_, message):
    # Get administrators
    administrators = []
    async for m in app.get_chat_members(
        message.chat.id, filter=ChatMembersFilter.ADMINISTRATORS
    ):
        administrators.append(m)
    if (message.from_user.id) in SUDOERS or (message.from_user.id) in [
        admin.user.id for admin in administrators
    ]:
        loop = await get_loop(message.chat.id)
        if loop == 0:
            await message.reply_text("Lopp is not enabled")
        else:
            try:
                await set_loop(message.chat.id, 0)
                await message.reply_text("Loop Disabled")
            except Exception as e:
                return await message.reply_text(f"Error:- <code>{e}</code>")
    else:
        return await message.reply_text(
            "Abe saale... (Maaf karna wo gusse me thora sa idhar udhar ho jata hu) terepe perms naa hai admins ko bol..."
  )
