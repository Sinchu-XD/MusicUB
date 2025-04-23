import requests
import os
from urllib.parse import urlparse, parse_qs
import yt_dlp
from YouTubeMusic.YtSearch import Search
import asyncio
import re

# ✅ Replace with your YouTube API Key
#YOUTUBE_API_KEY = "AIzaSyCfKI90y0KcrMIi-zlh9U0bYe9scFcJ9Vo"
#YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

# ✅ Path to your YouTube cookies file
COOKIES_FILE = "cookies/cookies.txt"


def searchYt(query: str) -> str:
    query = str(query)
    Result = await Search(query, limit=1)
    if not Result["result"] == []:
        title = Result["result"][0]["title"]
        duration = Result["result"][0]["duration"]
        link = Result["result"][0]["url"]
        return title, duration, link

    return None, None, None


def extract_playlist_id(url):
    """Extract playlist ID from YouTube URL."""
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("list", [None])[0]

def extract_video_id(url):
    """Extract video ID from YouTube URL."""
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]
    query_params = parse_qs(parsed_url.query)
    return query_params.get("v", [None])[0]

def parse_duration(duration_str):
    """Convert duration string like '12:34' or '1:02:45' to seconds."""
    parts = duration_str.split(':')
    parts = list(map(int, parts))
    if len(parts) == 3:
        hours, minutes, seconds = parts
    elif len(parts) == 2:
        hours = 0
        minutes, seconds = parts
    else:
        hours = 0
        minutes = 0
        seconds = parts[0]
    return hours * 3600 + minutes * 60 + seconds

def get_playlist_videos(playlist_url):
    """Fetch all videos from a YouTube playlist using youtube-search-python."""
    playlist = Playlist(playlist_url)
    playlist.videos  # Load initial videos

    videos = []

    while playlist.hasMoreVideos:
        playlist.getNextVideos()

    for video in playlist.videos:
        title = video['title']
        duration = parse_duration(video.get('duration', '0:00'))
        link = video['link']
        videos.append((title, duration, link))

    return videos


"""
def get_playlist_videos(playlist_id):
    playlist_items_url = f"{YOUTUBE_API_URL}/playlistItems"
    videos = []
    next_page_token = None

    while True:
        params = {
            "part": "snippet",
            "playlistId": playlist_id,
            "maxResults": 50,  # Fetch 50 videos per request (max limit)
            "key": YOUTUBE_API_KEY,
        }
        if next_page_token:
            params["pageToken"] = next_page_token

        response = requests.get(playlist_items_url, params=params)
        data = response.json()

        if "items" not in data or not data["items"]:
            break

        for item in data["items"]:
            video_id = item["snippet"]["resourceId"]["videoId"]
            title = item["snippet"]["title"]
            link = f"https://www.youtube.com/watch?v={video_id}"
            duration = get_video_duration(video_id)
            videos.append((title, duration, link))

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break  # Stop when no more pages

    return videos


def get_video_duration(video_id):
    video_url = f"{YOUTUBE_API_URL}/videos"
    params = {
        "part": "contentDetails",
        "id": video_id,
        "key": YOUTUBE_API_KEY,
    }
    
    response = requests.get(video_url, params=params)
    data = response.json()

    if "items" not in data or not data["items"]:
        return None
    
    duration = data["items"][0]["contentDetails"]["duration"]
    return parse_duration(duration)

def parse_duration(duration):
    import isodate  # Install with `pip install isodate`
    try:
        return int(isodate.parse_duration(duration).total_seconds())
    except:
        return None


def extract_playlist_id(url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("list", [None])[0]


def extract_video_id(url):
    parsed_url = urlparse(url)
    if parsed_url.hostname == "youtu.be":
        return parsed_url.path[1:]

    query_params = parse_qs(parsed_url.query)
    return query_params.get("v", [None])[0]
"""

async def ytdl(format: str, link: str):
    ydl_opts = {
        'format': format,
        'geo_bypass': True,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': COOKIES_FILE,  # Ensure cookies are used
        'nocheckcertificate': True,
        'force_generic_extractor': True,  # Force using a generic extractor if needed
        'extractor_retries': 3,  # Retry fetching if it fails
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=False)
            if 'url' in info:
                duration = info.get('duration', 0)  # Fetch duration safely
                return (1, info['url'], duration)

            else:
                return (0, "No URL found", 0)
    except Exception as e:
        return (0, str(e), 0)

def get_direct_audio_url(video_url):
    ydl_opts = {
        "format": "bestaudio",
        "quiet": False,  # ✅ Show errors if any
        "cookies": COOKIES_FILE,  # ✅ Use cookies
        "noplaylist": True,  # ✅ Avoid playlist issues
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=False)
            return info_dict.get("url", None) or "❌ yt-dlp Error: No URL found"
    except Exception as e:
        return f"❌ yt-dlp Error: {str(e)}"


# ✅ Example Usage:
if __name__ == "__main__":
    url = "https://www.youtube.com/playlist?list=PLxyz..."  # Replace with your playlist
    vids = get_playlist_videos(url)
    for title, duration, link in vids:
        print(f"{title} | {duration} sec | {link}")
