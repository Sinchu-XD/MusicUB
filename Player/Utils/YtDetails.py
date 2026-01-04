import os
import logging
from YouTubeMusic.Search import Search
from YouTubeMusic.Stream import get_stream_url

logging.basicConfig(level=logging.INFO)

# ─────────────────────────────
# COOKIES
# ─────────────────────────────
COOKIES_FILE = "cookies/cookies.txt" if os.path.exists("cookies/cookies.txt") else None


# ─────────────────────────────
# STREAM CACHES
# ─────────────────────────────
AUDIO_STREAM_CACHE = {}   # {youtube_url: audio_stream_url}
VIDEO_STREAM_CACHE = {}   # {youtube_url: video_stream_url}


# ─────────────────────────────
# SEARCH YOUTUBE
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
        "url": item.get("url"),
    }]

    return search_data, item.get("url")


# ─────────────────────────────
# AUDIO STREAM  (/play)
# ─────────────────────────────
async def ytdl_audio(url: str):
    # CACHE HIT
    if url in AUDIO_STREAM_CACHE:
        logging.info("⚡ Using cached AUDIO stream URL")
        return True, AUDIO_STREAM_CACHE[url]

    # CACHE MISS
    try:
        stream_url = get_stream_url(
            video_url=url,
            cookies_path=COOKIES_FILE,
            mode="audio"
        )

        if not stream_url:
            return False, "Failed to get audio stream URL"

        AUDIO_STREAM_CACHE[url] = stream_url
        logging.info("📌 Cached new AUDIO stream URL")

        return True, stream_url

    except Exception as e:
        logging.error(f"AUDIO stream error: {e}")
        return False, str(e)


# ─────────────────────────────
# VIDEO STREAM WITH SOUND  (/vplay)
# ─────────────────────────────
async def ytdl_video(url: str):
    # CACHE HIT
    if url in VIDEO_STREAM_CACHE:
        logging.info("⚡ Using cached VIDEO stream URL")
        return True, VIDEO_STREAM_CACHE[url]

    # CACHE MISS
    try:
        stream_url = get_stream_url(
            video_url=url,
            cookies_path=COOKIES_FILE,
            mode="video"
        )

        if not stream_url:
            return False, "Failed to get video stream URL"

        VIDEO_STREAM_CACHE[url] = stream_url
        logging.info("📌 Cached new VIDEO stream URL")

        return True, stream_url

    except Exception as e:
        logging.error(f"VIDEO stream error: {e}")
        return False, str(e)


# ─────────────────────────────
# TEST (OPTIONAL)
# ─────────────────────────────
if __name__ == "__main__":
    import asyncio

    async def main():
        query = input("Enter song / video name: ")

        _, youtube_url = await SearchYt(query)
        if not youtube_url:
            print("❌ No result found")
            return

        # AUDIO TEST
        s, a = await ytdl_audio(youtube_url)
        print("Audio:", "OK" if s else a)

        # VIDEO TEST
        s, v = await ytdl_video(youtube_url)
        print("Video:", "OK" if s else v)

    asyncio.run(main())
