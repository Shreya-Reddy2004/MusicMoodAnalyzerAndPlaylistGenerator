import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
import time

# Spotify API credentials
client_id = '6d21e265073649828becd73dc9878fee'
client_secret = '0b998d4cfb454e50b75cde2b33a2c803'

# Authenticate with the Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, requests_session=False)

# Define predefined moods
predefined_moods = ['Happy', 'Sad', 'Relaxed', 'Neutral']

# Function to get track features
def get_track_features(track_id):
    features = sp.audio_features(track_id)[0]
    return features

# Function to get tracks from a specific playlist
def get_tracks_from_playlist(playlist_id):
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']
    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])
    return tracks

# Dummy mood classification function
def classify_mood(features_df):
    def mood_classifier(row):
        if row['valence'] > 0.5 and row['energy'] > 0.5:
            return 'Happy'
        elif row['valence'] < 0.5 and row['energy'] < 0.5:
            return 'Sad'
        elif row['valence'] > 0.5 and row['energy'] < 0.5:
            return 'Relaxed'
        else:
            return 'Neutral'
    
    features_df['mood'] = features_df.apply(mood_classifier, axis=1)
    return features_df

# Function to create sub-playlists based on mood
def create_sub_playlists(mood_df):
    sub_playlists = {}
    for mood in predefined_moods:
        sub_playlists[mood] = mood_df[mood_df['mood'] == mood]
    return sub_playlists

# Function to get track preview URL and album artwork
def get_track_preview_and_artwork(track_id):
    track = sp.track(track_id)
    preview_url = track.get('preview_url')
    album_art_url = track['album']['images'][0]['url'] if track['album']['images'] else None
    return preview_url, album_art_url

# Streamlit app
def main():
    st.set_page_config(page_title="Spotify Playlist Analyzer", layout="wide")

    # Custom CSS for dark mode
    st.markdown(
        """
        <style>
        .css-18e3th9 {
            background-color: #333333;
        }
        .css-1d391kg {
            background-color: #333333;
        }
        .st-cz {
            background-color: #333333;
        }
        .st-de {
            color: #ffffff;
        }
        .st-fb {
            color: #ffffff;
        }
        .st-cx {
            background-color: #333333;
        }
        .st-ek {
            color: #ffffff;
        }
        .css-1ht1j8u {
            color: #ffffff;
        }
        .css-18ni7ap {
            color: #ffffff;
        }
        .css-2trqyj {
            color: #ffffff;
        }
        .css-81f9rf {
            background-color: #444444;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Sidebar
    with st.sidebar:
        st.header("Playlist Analyzer")
        playlist_id = st.text_input("Enter Spotify Playlist ID:")
        analyze_button = st.button("Analyze Playlist")
        st.header("Generate Playlist")
        mood = st.radio("Choose a mood:", predefined_moods)
        num_songs_input = st.text_input("Enter the number of songs you want in the playlist (only numbers):", value="10")
        generate_button = st.button("Generate Playlist")

    st.title("Spotify Playlist Analyzer and Mood Mapper")
    
    if analyze_button:
        if playlist_id:
            st.write("Fetching tracks from playlist...")

            # Collect track data
            track_data = []
            try:
                tracks = get_tracks_from_playlist(playlist_id)
                for i, item in enumerate(tracks):
                    track = item.get('track')
                    if track is None or track['id'] is None:
                        continue

                    track_id = track['id']
                    track_name = track['name']
                    artist_name = track['artists'][0]['name']

                    try:
                        features = get_track_features(track_id)
                        preview_url, album_art_url = get_track_preview_and_artwork(track_id)
                    except Exception as e:
                        st.error(f"Error getting features for track {track_id}: {e}")
                        continue

                    if features:
                        track_info = {
                            'track_name': track_name,
                            'artist_name': artist_name,
                            'acousticness': features['acousticness'],
                            'danceability': features['danceability'],
                            'energy': features['energy'],
                            'instrumentalness': features['instrumentalness'],
                            'liveness': features['liveness'],
                            'loudness': features['loudness'],
                            'speechiness': features['speechiness'],
                            'tempo': features['tempo'],
                            'valence': features['valence'],
                            'preview_url': preview_url,
                            'album_art_url': album_art_url
                        }
                        track_data.append(track_info)
                    
                    # To avoid hitting rate limits and to show progress
                    if i % 10 == 0:
                        st.write(f'Processed {i+1} tracks from playlist {playlist_id}')
                    time.sleep(0.5)
                    
            except Exception as e:
                st.error(f"An error occurred: {e}")

            # Convert track data to DataFrame
            if track_data:
                mood_df = pd.DataFrame(track_data)
                
                # Classify moods
                mood_df = classify_mood(mood_df)
                
                # Create sub-playlists based on mood
                sub_playlists = create_sub_playlists(mood_df)
                
                # Save DataFrame to CSV
                filename = 'playlist_tracks.csv'
                mood_df.to_csv(filename, index=False)
                
                st.success(f'Dataset has been saved to {filename}')
                st.write(f'Total tracks processed: {len(track_data)}')
                
                # Display mood mapping as a table
                st.subheader("Tracks with Mood Classification:")
                st.dataframe(mood_df[['track_name', 'artist_name', 'mood']])
                
                # Display sub-playlists
                st.subheader("Sub-Playlists by Mood:")
                for mood, songs in sub_playlists.items():
                    if not songs.empty:
                        st.write(f"**{mood} Songs:**")
                        for index, row in songs.iterrows():
                            st.write(f"**{row['track_name']}** by {row['artist_name']}")
                            # Display album artwork and audio preview
                            if pd.notna(row.get('album_art_url')):
                                st.image(row['album_art_url'], width=200)
                            if pd.notna(row.get('preview_url')):
                                st.audio(row['preview_url'])
                            # Display mood below
                            st.write(f"Mood: {row['mood']}")
            else:
                st.warning("No tracks found or an error occurred.")
        else:
            st.warning("Please enter a valid Spotify playlist ID.")

    if generate_button:
        try:
            num_songs = int(num_songs_input)
            if num_songs < 1:
                st.warning("Please enter a positive number.")
                return
        except ValueError:
            st.warning("Invalid input. Please enter a valid number.")
            return

        # Load the updated dataset (existing dataset)
        try:
            df = pd.read_csv('combined_songs_data.csv')
        except FileNotFoundError:
            st.warning("Dataset file not found.")
            return

        # Check the maximum number of available songs for the selected mood
        max_songs = df[df['mood'] == mood].shape[0]

        if num_songs > max_songs:
            st.warning(f"The maximum number of songs available for the selected mood '{mood}' is {max_songs}. Displaying the maximum available songs.")
            num_songs = max_songs

        # Create the playlist
        filtered_songs = df[df['mood'] == mood]
        filtered_songs = filtered_songs.drop_duplicates(subset=['track_name', 'artist_name'])
        playlist = filtered_songs.head(num_songs)

        if not playlist.empty:
            st.subheader(f"Your playlist for mood '{mood}':")
            for index, row in playlist.iterrows():
                st.write(f"**{row['track_name']}** by {row['artist_name']}")
                
                # Display album artwork and audio preview
                if pd.notna(row.get('album_art_url')):
                    st.image(row['album_art_url'], width=200)
                if pd.notna(row.get('preview_url')):
                    st.audio(row['preview_url'])
                
                # Display mood below
                st.write(f"Mood: {row['mood']}")
        
            # Save the playlist to a CSV file
            filename = f'playlist_{mood}.csv'
            try:
                playlist.to_csv(filename, index=False)
                st.success(f"Playlist saved to '{filename}'.")
                st.write(f"File Path: {filename}")  # Show file path for debugging
            except Exception as e:
                st.error(f"An error occurred while saving the file: {e}")
        else:
            st.warning("No songs available for the selected mood.")

if __name__ == "__main__":
    main()
