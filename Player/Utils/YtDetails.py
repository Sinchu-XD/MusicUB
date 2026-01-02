import os
import logging
from YouTubeMusic.Search import Search
from YouTubeMusic.Stream import get_audio_url

logging.basicConfig(level=logging.INFO)

COOKIES_FILE = "cookies/cookies.txt" if os.path.exists("cookies/cookies.txt") else None


# ─────────────────────────────
# SEARCH YOUTUBE MUSIC
# ─────────────────────────────
async def SearchYt(query: str):
    results = await Search(query, limit=1)

    if not results or not results.get("main_results"):
        return [], None

    item = results["main_results"][0]

    search_data = [{
        "title": item.get("title"),
        "duration": item.get("duration") or "Unknown",
        "thumbnail": item.get("thumbnail"),
        "url": item.get("url")
    }]

    return search_data, item.get("url")


# ─────────────────────────────
# GET AUDIO STREAM URL
# ─────────────────────────────
async def ytdl(url: str):
    try:
        stream_url = get_audio_url(url, COOKIES_FILE)
        if not stream_url:
            return False, "Failed to get stream URL"
        return True, stream_url
    except Exception as e:
        logging.error(f"YT stream error: {e}")
        return False, str(e)


async def main():
    query = input("Enter song name: ")
    try:
        search_results, youtube_url = await SearchYt(query)
        status, stream_url = await ytdl(youtube_url)
        
        if status:
            print(f"Stream URL ready to play: {stream_url}")
        else:
            print(f"Error: {stream_url}")
        
        for idx, item in enumerate(search_results, 1):
            print(f"\nResult {idx}:")
            print(f"Title: {item['title']}")
            print(f"Artist: {item['artist']}")
            print(f"Channel: {item['channel']}")
            print(f"Duration: {item['duration']}")
            print(f"Views: {item['views']}")
            print(f"Thumbnail: {item['thumbnail']}")
            print(f"URL: {item['url']}")
    
    except Exception as e:
        print(f"Search Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
    
