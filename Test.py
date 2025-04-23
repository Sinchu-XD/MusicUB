import asyncio
from Player.Utils.YtDetails import get_stream_url  # Update path if needed

async def main():
    query = "Never Gonna Give You Up"
    try:
        stream_url = await get_stream_url(query)
        print(f"✅ Stream URL for '{query}':\n{stream_url}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
