import requests
import os
import yt_dlp
from YouTubeMusic.YtSearch import Search
import asyncio
import re

COOKIES_FILE = "cookies/cookies.txt"

async def searchYt(query: str):
    query = str(query)
    Result = await Search(query, limit=1)

    if Result and "result" in Result and Result["result"]:
        title = Result["result"][0].get("title", "Unknown Title")
        duration = Result["result"][0].get("duration", "Unknown Duration")
        link = Result["result"][0].get("url", "No URL")
        return title, duration, link

    return None, None, None

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
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    loop = asyncio.get_event_loop()
    title, duration, link = loop.run_until_complete(searchYt("Never Gonna Give You Up"))
    if title:
        print(f"{title} | {link}")
        
