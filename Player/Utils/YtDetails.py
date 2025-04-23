import yt_dlp
import asyncio
from YouTubeMusic.YtSearch import Search

COOKIES_FILE = "cookies/cookies.txt"

async def get_stream_url(query: str) -> str:
    results = await Search(query, limit=1)
    if not results:
        raise Exception("No results found.")
    return results[0]["url"]

async def ytdl(format: str, url: str):
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
            info = ydl.extract_info(url, download=False)
            if 'url' in info:
                return (1, info['url'])
            else:
                return (0, "No URL found")
    except Exception as e:
        return (0, str(e))

if __name__ == "__main__":
    async def main():
        query = input("Enter song name: ")
        try:
            url = await get_stream_url(query)
            format = "bestaudio"
            status, stream_url = await ytdl(format, url)
            if status:
                print(f"Stream URL: {stream_url}")
            else:
                print(f"Error: {stream_url}")
        except Exception as e:
            print(f"Search Error: {e}")

    asyncio.run(main())
