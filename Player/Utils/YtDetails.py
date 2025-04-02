"""
Telegram @Itz_Your_4Bhi @NotReallyAbhi
Copyright ©️ 2025
"""

import requests
import os
from urllib.parse import urlparse, parse_qs
import yt_dlp

# ✅ Replace with your YouTube API Key
YOUTUBE_API_KEY = "AIzaSyAO-vb96xq-xyaYRTy9lF21rIINu67Snzg"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"

# ✅ Path to your YouTube cookies file
COOKIES_FILE = "cookies/cookies.txt"


def searchYt(query):
    """Search for a YouTube video using YouTube Data API v3."""
    search_url = f"{YOUTUBE_API_URL}/search"
    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": 1,
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(search_url, params=params)
    data = response.json()

    if "items" not in data or not data["items"]:
        return None, None, None

    video_id = data["items"][0]["id"]["videoId"]
    title = data["items"][0]["snippet"]["title"]
    link = f"https://www.youtube.com/watch?v={video_id}"

    # Fetch video duration
    duration = get_video_duration(video_id)

    return title, duration, link


def get_playlist_videos(playlist_id):
    """Fetch all videos from a YouTube playlist using YouTube Data API v3."""
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
    """Fetch video duration using YouTube API v3."""
    video_url = f"{YOUTUBE_API_URL}/videos"
    params = {
        "part": "contentDetails",
        "id": video_id,
        "key": YOUTUBE_API_KEY,
    }

    response = requests.get(video_url, params=params)
    data = response.json()

    if "items" not in data or not data["items"]:
        return "Unknown"

    duration_iso = data["items"][0]["contentDetails"]["duration"]

from yt_dlp import YoutubeDL

async def ytdl(format, link):
    ydl_opts = {
        'format': format,
        'geo_bypass': True,
        'noplaylist': True,
        'quiet': True,
        'cookiefile': "cookies/cookies.txt",  # Ensure cookies are used
        'nocheckcertificate': True,
        'force_generic_extractor': True,  # Force using a generic extractor if needed
        'extractor_retries': 3,  # Retry fetching if it fails
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = await asyncio.to_thread(ydl.extract_info, link)
            if 'formats' in info:
                songlink = next((f['url'] for f in info['formats'] if f['format_id'] == 'bestaudio'), None)
                duration = info.get('duration', None)
                return 1, songlink, duration
            else:
                return 0, None, None
    except Exception as e:
        return 0, None, None



def parse_duration(duration):
    """Convert YouTube's ISO 8601 duration format (PT#M#S) to MM:SS."""
    import re
    matches = re.match(r"PT(?:(\d+)M)?(?:(\d+)S)?", duration)
    minutes = int(matches[1]) if matches[1] else 0
    seconds = int(matches[2]) if matches[2] else 0
    return f"{minutes}:{seconds:02d}"


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




def get_direct_audio_url(video_url):
    """Fetch the direct audio URL using yt-dlp with cookies."""
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
    

    # ✅ Playlist Example
    playlist_url = "https://www.youtube.com/playlist?list=YOUR_PLAYLIST_ID"
    playlist_id = extract_playlist_id(playlist_url)
    videos = get_playlist_videos(playlist_id)

    if videos:
        print(f"✅ Found {len(videos)} videos in the playlist!")

        for title, duration, link in videos:
            audio_url = get_direct_audio_url(link)
            print(f"🎵 {title} ({duration}) - {audio_url}")
    else:
        print("❌ No videos found!")
