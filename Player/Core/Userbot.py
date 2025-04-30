"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""
import os
import asyncio
from Player import call
from pytgcalls.types import MediaStream, VideoQuality, AudioQuality

audio_file = "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"


async def playAudio(chat_id, audio_file=audio_file):
    try:
        await call.play(
            chat_id,
            MediaStream(
                media_path=audio_file,   
                audio_parameters=AudioQuality.STUDIO,
                video_flags=MediaStream.Flags.IGNORE,
            ),
        )
        return True, None
    except Exception as e:
        return False, f"Error: <code>{e}</code>"


async def playVideo(chat_id, video_file, quality="SD_480p"):
    try:
        quality_mapping = {
            "uhd_4k": VideoQuality.UHD_4K,
            "qhd_2k": VideoQuality.QHD_2K,
            "fhd_1080p": VideoQuality.FHD_1080p,
            "hd_720p": VideoQuality.HD_720p,
            "sd_480p": VideoQuality.SD_480p,
            "sd_360p": VideoQuality.SD_360p,
        }

        video_quality = quality_mapping.get(quality.lower(), VideoQuality.SD_480p)

        await call.play(
            chat_id,
            MediaStream(
                media_path=video_file,
                audio_parameters=AudioQuality.MEDIUM,
                video_parameters=video_quality,
            ),
        )

        return True, None

    except Exception as e:
        return False, f"Error: <code>{e}</code>"
        

async def generate_filtered_audio(chat_id, audio_file, filter_type):
    filtered_path = f"downloads/{chat_id}_{filter_type}.raw"

    if filter_type == "bass":
        filter_cmd = "bass=g=10"
    elif filter_type == "nightcore":
        filter_cmd = "asetrate=44100*1.25,atempo=1.1"
    elif filter_type == "vaporwave":
        filter_cmd = "asetrate=44100*0.8,atempo=0.9"
    else:
        return audio_file

    cmd = f"ffmpeg -y -i '{audio_file}' -af '{filter_cmd}' -f s16le -ac 2 -ar 48000 '{filtered_path}'"
    process = await asyncio.create_subprocess_shell(cmd)
    await process.communicate()

    return filtered_path


async def pause(chat_id):
    try:
        await call.pause(chat_id)
        return "⏸ Stream Paused"
    except Exception as e:
        return f"Error: <code>{e}</code>"


async def resume(chat_id):
    try:
        await call.resume(chat_id)
        return "▶️ Stream Resumed"
    except Exception as e:
        return f"Error: <code>{e}</code>"


async def mute(chat_id):
    try:
        await call.mute(chat_id)
        return "🔇 Stream Muted"
    except Exception as e:
        return f"Error: <code>{e}</code>"


async def unmute(chat_id):
    try:
        await call.unmute(chat_id)
        return "🔊 Stream Unmuted"
    except Exception as e:
        return f"Error: <code>{e}</code>"


async def change_volume(chat_id, volume: int = 200):
    try:
        await call.change_volume(chat_id, volume)
        return f"🎧 Volume Changed To: {volume}%"
    except Exception as e:
        return f"Error: <code>{e}</code>"


async def stop(chat_id):
    try:
        await call.leave_call(chat_id)
        return "🛑 Stream Ended"
    except Exception as e:
        return f"Error: <code>{e}</code>"
