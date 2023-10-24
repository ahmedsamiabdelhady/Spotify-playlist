from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CLIENT_ID = "YOUR CLIENT ID"
CLIENT_SECRET= "YOUR CLIENT SECRET"
redirect_uri= "YOUR REDIRECT URI"
scope= "playlist-modify-private"

date= input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: \n")
year= date.split("-")[0]

URL= f"https://www.billboard.com/charts/hot-100/{date}/"

response= requests.get(URL)
contents= response.text

# Make a list with a to 100 songs in inputed date.

soup= BeautifulSoup(contents, "html.parser")

top_songs= []
divs= soup.find_all(name="div", class_= "o-chart-results-list-row-container")
for div in divs:
    song= div.find(name="h3", class_="c-title").get_text(strip=True)
    top_songs.append(song)

#Create a playlist in Spotify.

spotify= spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=redirect_uri, scope=scope))

playlist_name = f"{date} Billboard 100"
playlist_id= spotify.user_playlist_create(spotify.me()['id'], name=playlist_name, public=False)["id"]
print(f"Playlist '{playlist_name}' created!")

#Make a list with a songs' URI.

songs_uri=[]
for song in top_songs:
    uri= spotify.search(q= f"track: {song} year: {year}", type= "track")['tracks']['items'][0]['uri']
    songs_uri.append(uri)
print("URIs list is done!")

#Adding the songs in the playlist.

spotify.playlist_add_items(playlist_id= playlist_id, items=songs_uri)
print("Your playlist is done!")