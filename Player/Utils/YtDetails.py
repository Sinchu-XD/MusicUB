import os
import hashlib
import logging
import yt_dlp
import asyncio
from YouTubeMusic.YtSearch import Search

COOKIES_FILE = "cookies/cookies.txt"
CACHE_DIR = 'cached_songs'

if not os.path.exists(CACHE_DIR):
    os.makedirs(CACHE_DIR)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


async def SearchYt(query: str):
    results = await Search(query, limit=1)

    if not results:
        raise Exception("No results found.")

    search_data = []
    for item in results:
        search_data.append({
            "title": item["title"],
            "artist": item["artist_name"],
            "channel": item["channel_name"],
            "duration": item["duration"],
            "views": item["views"],
            "thumbnail": item["thumbnail"],
            "url": item["url"]
        })

    stream_url = results[0]["url"]
    
    return search_data, stream_url

async def ytdl(format: str, url: str):
    hashed = hashlib.md5(url.encode()).hexdigest()
    cached_path = os.path.join(CACHE_DIR, f"{hashed}.webm")

    if os.path.exists(cached_path):
        logging.info(f"Cache hit for URL: {url}")
        return (1, cached_path)

    logging.info(f"Cache miss for URL: {url} - Downloading...")

    ydl_opts = {
        'format': format,
        'geo_bypass': True,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': COOKIES_FILE,
        'nocheckcertificate': True,
        'force_generic_extractor': True,
        'extractor_retries': 3,
        'outtmpl': cached_path,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            logging.info(f"Downloaded file: {cached_path}")
            return (1, cached_path)
    except Exception as e:
        logging.error(f"Error during download: {e}")
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
