import asyncio
from YouTubeMusic.YtSearch import get_stream_url

async def main():
    query = input("🔍 Enter search query: ")
    try:
        stream_url = await get_stream_url(query)
        print(f"✅ Stream URL:\n{stream_url}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
