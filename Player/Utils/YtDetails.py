import requests
import os
import yt_dlp
from YouTubeMusic.YtSearch import Search
import asyncio
import re

COOKIES_FILE = "cookies/cookies.txt"

YDL_OPTS = {
        'format': format,
        'geo_bypass': True,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': COOKIES_FILE,
        'nocheckcertificate': True,
        'force_generic_extractor': True,
        'extractor_retries': 3, 
}

async def get_stream_url(query: str) -> str:
    search_results = await Search(query, limit=1)
    if not search_results:
        raise Exception(f"Song '{query}' not found.")
    url = search_results[0]["url"]
    loop = asyncio.get_event_loop()
    data = await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(YDL_OPTS).extract_info(url, download=False))
    if "url" not in data:
        raise Exception(f"Failed to extract stream URL for '{query}'.")
    return data["url"]

async def ytdl(format: str, link: str):
    ydl_opts = {
        'format': format,
        'geo_bypass': True,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': COOKIES_FILE,
        'nocheckcertificate': True,
        'force_generic_extractor': True,
        'extractor_retries': 3, 
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            if 'url' in info:
                return (1, info['url'])
            else:
                return (0, "No URL found")
    except Exception as e:
        return (0, str(e))

if __name__ == "__main__":
    title, duration, link = asyncio.run(searchYt("Never Gonna Give You Up"))
    if title:
        print(f"{title} | {link}")
        
