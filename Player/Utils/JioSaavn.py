import requests

JIOSAAVN_API = "https://jiosaavn-api.vercel.app"  # Public JioSaavn API

def get_song(query):
    """Fetch song details from JioSaavn API."""
    url = f"{JIOSAAVN_API}/search?query={query}"
    response = requests.get(url).json()
    
    if not response or "data" not in response:
        return None

    song = response["data"][0]
    return {
        "title": song["title"],
        "url": song["url"],
        "media_url": song["media_url"],
        "thumbnail": song["image"],
        "artist": song["primaryArtists"]
    }
  
