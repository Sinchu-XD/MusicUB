"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from Player import call
from pytgcalls.types import MediaStream, VideoQuality, AudioQuality

audio_file = "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"


async def playAudio(chat_id, audio_file=audio_file):
    """Plays an audio file in the given chat."""
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


async def playVideo(chat_id, video_file=audio_file):
    """Plays a video file in the given chat."""
    try:
        await call.play(
            chat_id,
            MediaStream(
                media_path=video_file,
                audio_parameters=AudioQuality.STUDIO,
                video_parameters=VideoQuality.UHD_4K,  # Corrected this part
            ),
        )
        return True, None
    except Exception as e:
        return False, f"Error: <code>{e}</code>"


async def pause(chat_id):
    """Pauses the stream."""
    try:
        await call.pause_stream(chat_id)
        return "⏸ Stream Paused"
    except Exception as e:
        return f"Error: <code>{e}</code>"


async def resume(chat_id):
    """Resumes the paused stream."""
    try:
        await call.resume_stream(chat_id)
        return "▶️ Stream Resumed"
    except Exception as e:
        return f"Error: <code>{e}</code>"


async def mute(chat_id):
    """Mutes the stream."""
    try:
        await call.mute_stream(chat_id)
        return "🔇 Stream Muted"
    except Exception as e:
        return f"Error: <code>{e}</code>"


async def unmute(chat_id):
    """Unmutes the stream."""
    try:
        await call.unmute_stream(chat_id)
        return "🔊 Stream Unmuted"
    except Exception as e:
        return f"Error: <code>{e}</code>"


async def changeVolume(chat_id, volume: int = 200):
    """Changes the stream volume."""
    try:
        await call.change_volume_call(chat_id, volume)
        return f"🎧 Volume Changed To: {volume}%"
    except Exception as e:
        return f"Error: <code>{e}</code>"


async def stop(chat_id):
    """Stops the stream and leaves the voice chat."""
    try:
        await call.leave_call(chat_id)
        return "🛑 Stream Ended"
    except Exception as e:
        return f"Error: <code>{e}</code>"
        
