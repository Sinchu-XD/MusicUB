from motor.motor_asyncio import AsyncIOMotorClient
import config

client = AsyncIOMotorClient(config.MONGO_URI)
db = client["MusicBot"]

search_collection = db["search_cache"]
stream_collection = db["stream_cache"]
