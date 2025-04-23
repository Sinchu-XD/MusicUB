import asyncio
from Player.Utils.YtDetails import SearchYt

async def main():
    query = input("🔍 Enter search query: ")
    try:
        stream_url = await SearchYt(query)
        print(f"✅ URL:\n{stream_url}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
