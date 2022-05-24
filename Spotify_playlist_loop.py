import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time
import pandas as pd

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="YOUR WEB APP CREDENTIALS",
                                                           client_secret="YOUR WEB APP CREDENTIALS"))

def getTrackIDs(playlist_id):
    track_ids = []
    playlist = sp.playlist(playlist_id)
    for item in playlist['tracks']['items']:
        track = item['track']
        track_ids.append(track['id'])
    return(track_ids)

def getTrackFeatures(id):
    track_info = sp.track(id)
    features_info = sp.audio_features(id)

    #Artist ID for specific song
    artist_id = track_info['artists'][0]['id']
    artist_info = sp.artist(artist_id)

    #Track info
    name = track_info['name']
    length = track_info['duration_ms']
    popularity = track_info['popularity']
    album_dict = track_info['album']
    album = album_dict['name']
    release_date = album_dict['release_date']
    artist = album_dict['artists'][0]['name']
    artist_followers = artist_info['followers']['total']
    genre = artist_info['genres']

    #Track Features
    feature_dict = features_info[0]
    acousticness = feature_dict['acousticness']
    danceability = feature_dict['danceability']
    energy = feature_dict['energy']
    instrumentalness = feature_dict['instrumentalness']
    key = feature_dict['key']
    liveness = feature_dict['liveness']
    loudness = feature_dict['loudness']
    mode = feature_dict['mode']
    speechiness = feature_dict['speechiness']
    tempo = feature_dict['tempo']
    time_signature = feature_dict['time_signature']
    valence = feature_dict['valence']

    track_data = [id,name,artist,artist_followers,genre,album,release_date,length,popularity,
                acousticness,danceability,energy,instrumentalness,key,liveness,loudness,mode,speechiness,tempo,time_signature,valence]

    return(track_data)

# Single playlist
def createDataFrame(playlist, df_name):
    track_ids = getTrackIDs(playlist)
    track_list = []
    for i in range(len(track_ids)):
        time.sleep(.3)
        track_data = getTrackFeatures(track_ids[i])
        track_list.append(track_data)

    playlist_data = pd.DataFrame(track_list, columns =['spotifty id','name','artist','artist followers','genre','album','release_date','length','popularity',
                'acousticness','danceability','energy','instrumentalness','key','liveness','loudness','mode','speechiness','tempo','time_signature','valence'])

    playlist_data.to_csv(df_name, index=False)

# Array of multiple playlist
def createStack(array_of_pl_urn, file_name):
    track_list = []
    for playlist in array_of_pl_urn:
        track_ids = getTrackIDs(playlist)
        for i in range(len(track_ids)):
            time.sleep(.3)
            track_data = getTrackFeatures(track_ids[i])
            track_list.append(track_data)

    stacked_df = pd.DataFrame(track_list, columns =['spotifty id','name','artist','artist followers','genre','album','release_date','length','popularity',
                'acousticness','danceability','energy','instrumentalness','key','liveness','loudness','mode','speechiness','tempo','time_signature','valence'])

    stacked_df.to_csv(file_name, index=False)

#-----------WHERE USER PUT INFORMATION-----------------

# For a single playlist in a CSV file
WakeUpHappy_urn = 'spotify:user:spotifycharts:playlist:37i9dQZF1DX0UrRvztWcAU?si=401127a7e1094a7c'
AmbientRelaxation_urn = 'spotify:user:spotifycharts:playlist:37i9dQZF1DX3Ogo9pFvBkY?si=1ba47305f1f04cbb'

createDataFrame(WakeUpHappy_urn, 'WakeUpHappy.csv')
createDataFrame(AmbientRelaxation_urn, 'AmbientRelaxation.csv')

# For multiple playlists stacked in one CSV file
list_of_urn = [WakeUpHappy_urn, AmbientRelaxation_urn]
createStack(list_of_urn, "stacked_playlist.csv")