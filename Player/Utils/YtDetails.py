import os
import hashlib
import logging
import yt_dlp
import asyncio
from YouTubeMusic.Search import Search
from YouTubeMusic.Stream import get_audio_url


COOKIES_FILE = "cookies/cookies.txt"
CACHE_DIR = 'cached_songs'

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def SearchYt(query: str):
    results = await Search(query, limit=1)

    if not results or not results.get("main_results"):
        raise Exception("No results found.")

    item = results["main_results"][0] 

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

    return search_data, stream_url


import os
import hashlib
import aiohttp
import logging
from YouTubeMusic.Stream import get_audio_url

CACHE_DIR = "downloads"
os.makedirs(CACHE_DIR, exist_ok=True)

async def ytdl(url: str):
    hashed = hashlib.md5(url.encode()).hexdigest()
    cached_path = os.path.join(CACHE_DIR, f"{hashed}.webm")

    if os.path.exists(cached_path):
        logging.info(f"[CACHE HIT] {url}")
        return (1, cached_path)

    logging.info(f"[CACHE MISS] Fetching URL via get_audio_url()")

    try:
        stream_url = get_audio_url(url, "cookies/cookies.txt")
        if not stream_url:
            return (0, "Failed to get audio stream URL")

        async with aiohttp.ClientSession() as session:
            async with session.get(stream_url) as resp:
                if resp.status != 200:
                    return (0, f"HTTP error: {resp.status}")
                with open(cached_path, "wb") as f:
                    while chunk := await resp.content.read(1024 * 64):
                        f.write(chunk)

        logging.info(f"[DOWNLOADED] {cached_path}")
        return (1, cached_path)

    except Exception as e:
        logging.error(f"[ERROR] {e}")
        return (0, str(e))


async def main():
    query = input("Enter song name: ")
    try:
        search_results, stream_url = await SearchYt(query)
        format = "ba"
        status, stream_url = await ytdl(format, stream_url)
        
        if status:
            print(f"Stream URL: {stream_url}")
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
