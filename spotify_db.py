from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pandas as pd
import matplotlib.pyplot as plt
import re
import pymysql

# Spotify credentials
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id='',
    client_secret=''
))

# Database configuration using pymysql
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Root',
    'database': 'spotify_db'
}

# Establishing connection using pymysql
connection = pymysql.connect(**db_config)
cursor = connection.cursor()

# Spotify track URL and extraction
track_url = 'https://open.spotify.com/track/003vvx7Niy0yvhvHt4a68B'
track_id = re.search(r'track/([a-zA-Z0-9]+)', track_url).group(1)
track = sp.track(track_id)

# Extracting track data
track_data = {
    'Track Name': track['name'],
    'Artist': track['artists'][0]['name'],
    'Album': track['album']['name'],
    'Popularity': track['popularity'],
    'Duration(minutes)': track['duration_ms'] / 60000
}

# SQL Insert query
insert_query = """
INSERT INTO spotify_tracks (track_name, artist, album, popularity, duration_minutes)
VALUES (%s, %s, %s, %s, %s)
"""

cursor.execute(insert_query, (
    track_data['Track Name'],
    track_data['Artist'],
    track_data['Album'],
    track_data['Popularity'],
    track_data['Duration(minutes)']
))

# Commit and close
connection.commit()
print(f"Track '{track_data['Track Name']}' by {track_data['Artist']} inserted into the database.")

cursor.close()
connection.close()
