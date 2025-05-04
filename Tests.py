import asyncio
from Player import call
from Player.Core.Userbot import playAudio
from pytgcalls.types import MediaStream, VideoQuality, AudioQuality

chat_id = "-1002523755325" 
audio_file = "http://docs.evostream.com/sample_content/assets/sintel1m720p.mp4"  # Your audio file

# Function to start the call
async def start_call():
    try:
        # Start the call without chat_id as argument
        await call.start()
        print("Call started successfully!")
    except Exception as e:
        print(f"Error starting call: {e}")

# Function to play audio
async def play_audio():
    try:
        # Ensure the call is started first
        await start_call()

        # Play the audio after starting the call
        result, error = await playAudio(chat_id, audio_file)
        if result:
            print("Audio playing successfully!")
        else:
            print(f"Failed to play audio: {error}")
    except Exception as e:
        print(f"Error during audio playback: {e}")

# Main entry to handle the event loop
def main():
    # Ensure we run the asyncio code in the same event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(play_audio())

if __name__ == "__main__":
    main()
