"""

"""

import os
from Player import app
from Player.Core import Userbot
from Player.Utils.YtDetails import searchYt, extract_video_id
from Player.Utils.Queue import QUEUE, add_to_queue
from Player.Misc import SUDOERS

from pyrogram import filters

from pytgcalls.types import MediaStream

import asyncio
import random
import time

import config

VIDEO_PLAY = ["VP", "VPLAY"]

PREFIX = config.PREFIX

RPREFIX = config.RPREFIX

def cookies():
    folder_path = f"{os.getcwd()}/cookies"
    txt_files = glob.glob(os.path.join(folder_path, "*.txt"))
    if not txt_files:
        raise FileNotFoundError("No .txt files found in the specified folder.")
    cookie_txt_file = random.choice(txt_files)
    return f"""cookies/{str(cookie_txt_file).split("/")[-1]}"""
    

async def ytdl(link):
    proc = await asyncio.create_subprocess_exec(
        "yt-dlp",
        "-g",
        "-f",
        "best[height<=?720][width<=?1280]",
        f"--cookies {cookies()}"
        f"{link}",
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()
    if stdout:
        return 1, stdout.decode().split("\n")[0]
    else:
        return 0, stderr.decode()


async def processReplyToMessage(message):
    msg = message.reply_to_message
    if msg.video or msg.video_note:
        m = await message.reply_text("Rukja...Tera Video Download kar raha hu...")
        video_original = await msg.download()
        return video_original, m
    else:
        return None


async def playWithLinks(link):
    if "&" in link:
        pass
    if "?" in link:
        pass

    return 0


@app.on_message((filters.command(VIDEO_PLAY, [PREFIX, RPREFIX])) & filters.group)
async def _vPlay(_, message):
    start_time = time.time()
    chat_id = message.chat.id
    if (message.reply_to_message) is not None:
        if message.reply_to_message.video or message.reply_to_message.video_note:
            input_filename, m = await processReplyToMessage(message)
            if input_filename is None:
                return await message.reply_text(
                    "Video pe reply kon karega mai? ya phir video link kon dalega mai? 🤔"
                )
                
            await m.edit("Rukja...Tera Video Play kar raha hu...")
            Status, Text = await Userbot.playVideo(chat_id, input_filename)
            if Status == False:
                await m.edit(Text)
            
            else:
                video = message.reply_to_message.video or message.reply_to_message.video_note
                video_title = message.reply_to_message.text or "Unknown"
                await message.delete()
                if chat_id in QUEUE:
                    queue_num = add_to_queue(
                        chat_id,
                        video_title[:19],
                        video.duration,
                        video.file_id,
                        message.reply_to_message.link,
                    )
                    await m.edit(
                        f"# {queue_num}\n{video_title[:19]}\nTera video queue me daal diya hu"
                    )
                    return
                finish_time = time.time()
                total_time_taken = str(int(finish_time - start_time)) + "s"
                await m.edit(
                    f"Tera video play kar rha hu aaja vc\n\nVideoName:- [{video_title[:19]}]({message.reply_to_message.link})\nDuration:- {video.duration}\nTime taken to play:- {total_time_taken}",
                    disable_web_page_preview=True,
                )

    elif (len(message.command)) < 2:
        await message.reply_text("Link kon daalega mai? 🤔")
    else:
        m = await message.reply_text("Rukja...Tera video dhund raha hu...")
        query = message.text.split(maxsplit=1)[1]
        video_id = extract_video_id(query)
        try:
            if video_id is None:
                video_id = query
            title, duration, link = searchYt(video_id)
            if (title, duration, link) == (None, None, None):
                return await m.edit("No results found")
        except Exception as e:
            await message.reply_text(f"Error:- <code>{e}</code>")
            return

        await m.edit("Rukja...Tera video download kar raha hu...")
        resp, ytlink = await ytdl(link)
        if resp == 0:
            await m.edit(f"❌ yt-dl issues detected\n\n» `{ytlink}`")
        else:
            if chat_id in QUEUE:
                queue_num = add_to_queue(chat_id, title[:19], duration, ytlink, link)
                await m.edit(
                    f"# {queue_num}\n{title[:19]}\nTera Video queue me daal diya hu"
                )
                return
            # await asyncio.sleep(2)
            Status, Text = await Userbot.playVideo(chat_id, ytlink)
            # Check if the video ended
            if Status == False:
                return await m.edit(Text)
            if duration is None:
                duration = "Playing From LiveStream"
            add_to_queue(chat_id, title[:19], duration, ytlink, link)
            finish_time = time.time()
            total_time_taken = str(int(finish_time - start_time)) + "s"
            await m.edit(
                f"Playing your video\n\nVideoName:- [{title[:19]}]({link})\nDuration:- {duration}\nTime taken to play:- {total_time_taken}",
                disable_web_page_preview=True,
            )
