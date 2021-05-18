from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os


SPOTIFY_CLIENT_ID = os.environ.get('SECRET_ID')
SPOTIFY_CLIENT_SECRET = os.environ.get('SECRET_CLIENT')

APP_URL = f"https://developer.spotify.com/dashboard/applications/{SPOTIFY_CLIENT_ID}"


date = input("which year do you want ot travel to? Type date in this format YYYY-MM-DD: ")

# Scraping songs from billboard 100
data = requests.get(f"https://www.billboard.com/charts/hot-100/{date}")
soup = BeautifulSoup(data.text, "html.parser")
song_data = soup.find_all("span", class_="chart-element__information__song text--truncate color--primary")
songs = [song.getText() for song in song_data]

# Spotify Auth
sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_CLIENT_SECRET,
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
print(user_id)

# Searching spotify by song name
song_uris = []
year = date.split("-")[0]
for song in songs:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# new playlist
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)
# adding songs into playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)