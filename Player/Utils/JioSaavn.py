import re
import requests

JIOSAAVN_API = "https://saavn.me/songs?id={song_id}"

def extract_song_id(link):
    """Extract song ID from a JioSaavn link."""
    match = re.search(r"/song/[^/]+/(\w+)", link)
    return match.group(1) if match else None

def get_song(song_link):
    """Fetch song details from JioSaavn API."""
    song_id = extract_song_id(song_link)
    if not song_id:
        return None

    url = JIOSAAVN_API.format(song_id)
    response = requests.get(url).json()

    if "error" in response:
        return None

    return {
        "title": response.get("song"),
        "url": response.get("perma_url"),
        "media_url": response.get("media_url"),
        "thumbnail": response.get("image"),
        "artist": response.get("singers")
    }
