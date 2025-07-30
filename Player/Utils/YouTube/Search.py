import asyncio
from YouTubeMusic.Search import Search
from Player.Database import ensure_indexes, get_cached_search, add_cached_search

async def SearchYt(query: str):
    await ensure_indexes()
    normalized = query.lower().strip()
    cached = await get_cached_search(normalized)
    if cached:
        item = cached["result"]
    else:
        res = await Search(query, limit=1)
        if not res or not res.get("main_results"):
            raise Exception("No results found")
        item = res["main_results"][0]
        await add_cached_search(normalized, item)

    return [{
        "title": item.get("title"),
        "artist": item.get("artist_name"),
        "channel": item.get("channel_name"),
        "duration": item.get("duration"),
        "views": item.get("views"),
        "thumbnail": item.get("thumbnail"),
        "url": item.get("url"),
    }], item.get("url")
