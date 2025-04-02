import requests
import re
from bs4 import BeautifulSoup

JIOSAAVN_SEARCH_URL = "https://www.jiosaavn.com/search/{}"

def fetch_song_url(song_name):
    """Search JioSaavn and fetch the first song's URL."""
    search_url = JIOSAAVN_SEARCH_URL.format(song_name.replace(" ", "%20"))
    headers = {"User-Agent": "Mozilla/5.0"}

    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    song_links = soup.find_all("a", class_="u-color-js-gray")  # Find song links

    if not song_links:
        return None

    song_link = "https://www.jiosaavn.com" + song_links[0]["href"]  # First song link
    return song_link

def extract_mp3(song_link):
    """Extract the MP3 URL from the JioSaavn song page."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(song_link, headers=headers)

    if response.status_code != 200:
        return None

    song_id = re.search(r"song/[^/]+/(\w+)", song_link)
    if not song_id:
        return None

    api_url = f"https://www.jiosaavn.com/api.php?__call=song.getDetails&cc=in&_format=json&pids={song_id.group(1)}"
    song_data = requests.get(api_url, headers=headers).json()

    if not song_data:
        return None

    song_info = list(song_data.values())[0]
    return {
        "title": song_info["title"],
        "media_url": song_info["media_preview_url"].replace("_96_p.mp4", "_320.mp3"),  # Get high-quality MP3
        "artist": song_info["primary_artists"]
    }
