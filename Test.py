import asyncio
from Player.Utils.YtDetails import searchYt, ytdl

async def main():
    query = "Never Gonna Give You Up"
    title, duration, link = await searchYt(query)
    
    if not link:
        print("❌ No video found.")
        return

    print(f"🔍 Found: {title} ({duration})\n🔗 Link: {link}")

    status, audio_url = await ytdl("bestaudio", link)
    if status:
        print(f"✅ Direct audio URL: {audio_url}")
    else:
        print(f"❌ yt-dlp failed: {audio_url}")

if __name__ == "__main__":
    asyncio.run(main())
  
