"""
Telegram @Itz_Your_4Bhi
Copyright ©️ 2025
"""

from youtubesearchpython import VideosSearch, PlaylistsSearch
from urllib.parse import urlparse, parse_qs


def searchYt(query):
    """
    Search for a single video on YouTube.
    Returns: (title, duration, link) or (None, None, None)
    """
    query = str(query)
    videosResult = VideosSearch(query, limit=1)
    Result = videosResult.result()

    if Result and "result" in Result and Result["result"]:
        video = Result["result"][0]
        return video.get("title"), video.get("duration"), video.get("link")

    return None, None, None


def searchPlaylist(query):
    """
    Search for a YouTube playlist.
    Returns: (title, videoCount, link) or (None, None, None)
    """
    query = str(query)
    playlistResult = PlaylistsSearch(query, limit=1)
    Result = playlistResult.result()

    if Result and "result" in Result and Result["result"]:
        playlist = Result["result"][0]
        return playlist.get("title"), playlist.get("videoCount"), playlist.get("link")

    return None, None, None


def extract_playlist_id(url):
    """
    Extracts playlist ID from a YouTube URL.
    Returns: Playlist ID (str) or None
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    return query_params.get("list", [None])[0]  # FIXED: Added return statement


def extract_video_id(url):
    """
    Extracts video ID from a YouTube URL.
    Returns: Video ID (str) or None
    """
    parsed_url = urlparse(url)

    if parsed_url.hostname in ["youtu.be", "www.youtu.be"]:
        return parsed_url.path[1:]  # Shortened URL case

    query_params = parse_qs(parsed_url.query)
    return query_params.get("v", [None])[0]  # Regular YouTube video URL case
