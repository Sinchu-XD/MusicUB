"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

import requests
from urllib.parse import urlparse, parse_qs

# Get your YouTube API Key from https://console.developers.google.com/
YOUTUBE_API_KEY = "AIzaSyCVYsP4Ip49UlLzubYlv1ZnD2osWnMu32Y"
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"


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
    """Fetch all videos from a YouTube playlist."""
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
    return parse_duration(duration_iso)


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
