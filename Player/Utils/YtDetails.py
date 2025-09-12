import asyncio
import logging
from YouTubeMusic.Search import Search
from YouTubeMusic.Stream import get_audio_url

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

COOKIES_FILE = "cookies/cookies.txt"

async def SearchYt(query: str):
    print(f"[SearchYt] 🔍 Searching for query: {query}")
    results = await Search(query, limit=1)

    if not results or not results.get("main_results"):
        print("[SearchYt] ❌ No results found.")
        raise Exception("No results found.")

    item = results["main_results"][0]  
    print(f"[SearchYt] ✅ Got result: {item.get('title')}")

    search_data = [{
        "title": item.get("title"),
        "artist": item.get("artist_name"),
        "channel": item.get("channel_name"),
        "duration": item.get("duration"),
        "views": item.get("views"),
        "thumbnail": item.get("thumbnail"),
        "url": item.get("url")
    }]

    stream_url = item["url"]  
    print(f"[SearchYt] 🎵 Stream URL found: {stream_url}")

    return search_data, stream_url


async def ytdl(url: str):
    """
    Directly get audio stream URL without downloading.
    """
    print(f"[ytdl] 🔗 Processing URL: {url}")

    try:
        stream_url = get_audio_url(url, COOKIES_FILE)
        if not stream_url:
            print("[ytdl] ❌ Failed to get stream URL")
            return 0, "Failed to get audio stream URL"
        print(f"[ytdl] 🎵 Stream URL ready: {stream_url}")
        return 1, stream_url
    except Exception as e:
        print(f"[ytdl] ❌ ERROR: {e}")
        return 0, str(e)


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
    
