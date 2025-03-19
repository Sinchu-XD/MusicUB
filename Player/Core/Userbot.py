"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from Player import call
from pytgcalls.types import MediaStream, VideoQuality, AudioQuality
from Player.Utils.Queue import QUEUE  # Import Queue
import asyncio


audio_file = "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"


async def playAudio(chat_id, audio_file=audio_file):
    """Plays an audio file in VC."""
    try:
        await call.play(
            chat_id,
            MediaStream(
                audio_file,
                audio_parameters=AudioQuality.STUDIO,
                video_flags=MediaStream.Flags.IGNORE,
            ),
        )

        
    except Exception as e:
        return False, f"Error:- <code>{e}</code>"


async def playVideo(chat_id, video_file=audio_file):
    """Plays a video file in VC."""
    try:
        await call.play(
            chat_id,
            MediaStream(
                media_path=video_file,
                audio_parameters=AudioQuality.STUDIO,
                video_parameters=VideoQuality.UHD_4K,
            ),
        )
        
        
    except Exception as e:
        return False, f"Error:- <code>{e}</code>"


async def pause(chat_id):
    """Pauses the stream."""
    try:
        await call.pause_stream(chat_id)
        return "Stream Paused"
    except Exception as e:
        return f"Error:- <code>{e}</code>"


async def resume(chat_id):
    """Resumes the stream."""
    try:
        await call.resume_stream(chat_id)
        return "Stream Resumed"
    except Exception as e:
        return f"Error:- <code>{e}</code>"


async def mute(chat_id):
    """Mutes the stream."""
    try:
        await call.mute_stream(chat_id)
        return "Stream Muted"
    except Exception as e:
        return f"Error:- <code>{e}</code>"


async def unmute(chat_id):
    """Unmutes the stream."""
    try:
        await call.unmute_stream(chat_id)
        return "Stream Unmuted"
    except Exception as e:
        return f"Error:- <code>{e}</code>"


async def changeVolume(chat_id, volume: int = 200):
    """Changes the volume of the stream."""
    try:
        await call.change_volume_call(chat_id, volume)
        return f"🎧 Volume Changed To: {volume}%"
    except Exception as e:
        return f"Error:- <code>{e}</code>"


async def stop(chat_id):
    """Stops the stream and leaves the VC."""
    try:
        await call.leave_call(chat_id)
        
        # Remove chat from queue after stopping
        if chat_id in QUEUE:
            del QUEUE[chat_id]

        return "Stream Ended & Bot Left the VC"
    except Exception as e:
        return f"Error:- <code>{e}</code>"



