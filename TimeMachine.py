import pprint
import requests
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from datetime import datetime

from spotipy.oauth2 import SpotifyOAuth
import spotipy
load_dotenv()  # Load environment variables from .env file


date = input("What time do you want to travel to? (YYYY-MM-DD): ")
try:
    datetime.strptime(date, "%Y-%m-%d")  # Validate date format
except ValueError:
    print("Invalid date format. Please use YYYY-MM-DD.")
    exit()

header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"}

#Get the top 100
website = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/", headers=header).text #Scrape the Billboard Hot 100 chart for the given date
soup = BeautifulSoup(website, "html.parser") #Parse

songs = soup.select("li ul li h3") #Find all the song title elements (h3 which is inside li which is inside ul which is inside li)
song_names = [song.get_text(strip=True) for song in songs] #For each song in the songs list, get its text and strip it (remove useless space)

#Make it a spotify playlist

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private playlist-modify-public",
    redirect_uri="https://burakenterprises.github.io/spotify-redirect/",
    client_id=os.getenv('clientID'),
    client_secret=os.getenv('clientSecret'),
))

print(f"🎵 Creating your playlist from {date}...")
playlist = sp.user_playlist_create(user=sp.me()['id'], name=f"Time Machine - {date}", public=False, description=f"Top 100 songs from {date}") #Create a new playlist
for song in song_names:
    results = sp.search(q=song, type='track', limit=1)
    if results['tracks']['items']:
        uri= results['tracks']['items'][0]['uri']
        sp.playlist_add_items(playlist_id=playlist['id'], items=[uri])
        print(f"✅Added '{song}'")
    else:
        print(f"❌Song '{song}' not found on Spotify. Skipping.")
print(f"🎉 Playlist '{playlist['name']}' created successfully! You can find it in your Spotify library.")
