import os
import logging
from YouTubeMusic.Search import Search
from YouTubeMusic.Stream import get_audio_url

logging.basicConfig(level=logging.INFO)

COOKIES_FILE = "cookies/cookies.txt" if os.path.exists("cookies/cookies.txt") else None

# ─────────────────────────────
# UNLIMITED STREAM CACHE
# ─────────────────────────────
STREAM_CACHE = {}   # {youtube_url: stream_url}


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
# GET AUDIO STREAM URL (UNLIMITED CACHE)
# ─────────────────────────────
async def ytdl(url: str):
    # ───── CACHE HIT ─────
    if url in STREAM_CACHE:
        logging.info("⚡ Using cached stream URL")
        return True, STREAM_CACHE[url]

    # ───── CACHE MISS ─────
    try:
        stream_url = get_audio_url(url, COOKIES_FILE)
        if not stream_url:
            return False, "Failed to get stream URL"

        STREAM_CACHE[url] = stream_url
        logging.info("📌 Cached new stream URL (unlimited)")

        return True, stream_url

    except Exception as e:
        logging.error(f"YT stream error: {e}")
        return False, str(e)


# ─────────────────────────────
# TEST (OPTIONAL)
# ─────────────────────────────
if __name__ == "__main__":
    import asyncio

    async def main():
        query = input("Enter song name: ")
        search_results, youtube_url = await SearchYt(query)

        if not youtube_url:
            print("No result found")
            return

        status, stream_url = await ytdl(youtube_url)
        print("1st call:", "OK" if status else stream_url)

        status, stream_url = await ytdl(youtube_url)
        print("2nd call (cached):", "OK" if status else stream_url)

    asyncio.run(main())
