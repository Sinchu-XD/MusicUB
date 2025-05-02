import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials(client_id='529f0435df1c4770bbb719586ee9e710', client_secret='f578063466894149960027b193618eb3')
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

async def spotify_search(query):
    try:
        results = sp.search(q=query, type='track', limit=1) 
        
        if results['tracks']['items']:
            track = results['tracks']['items'][0]
            song_title = track['name']
            song_url = track['external_urls']['spotify']
            artist_name = track['artists'][0]['name']
            album_name = track['album']['name']
            song_duration = track['duration_ms'] / 1000

            return {
                'status': True,
                'title': song_title,
                'artist': artist_name,
                'album': album_name,
                'url': song_url,
                'duration': song_duration
            }
        else:
            return {
                'status': False,
                'message': "No results found for the query."
            }
    except Exception as e:
        return {
            'status': False,
            'message': f"Error searching Spotify: {e}"
        }
      
