import asyncio
from Player import call
from Player.Core.Userbot import playAudio
from pytgcalls.types import MediaStream, VideoQuality, AudioQuality

chat_id = "-1002523755325"
audio_file = "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"

# Functions
async def play_audio():
    try:
        result, error = await playAudio(chat_id, audio_file)
        if result:
            print("Audio playing successfully!")
        else:
            print(f"Failed to play audio: {error}")
    except Exception as e:
        print(f"Error during audio playback: {e}")

if __name__ == "__main__":
    asyncio.run(main())
