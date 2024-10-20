import streamlit as st
import speech_recognition as sr
import os
from pygame import mixer

# Initialize pygame mixer for playing audio
mixer.init()

# Path to your locally stored songs
SONGS_DIR = "songs"  # Folder where songs are stored

# List of available songs
available_songs = {
    "song one": "song1.mp3",
    "song two": "song2.mp3",
    "song3": "song3.mp3"
}

# Function to play song
def play_song(song_name):
    song_path = os.path.join(SONGS_DIR, available_songs[song_name])
    if os.path.exists(song_path):
        mixer.music.load(song_path)
        mixer.music.play()
        st.write(f"Now Playing: {song_name}")
    else:
        st.write("Sorry, song not found.")

# Handle recognized voice command for music
def handle_music_command(command):
    for song_name in available_songs.keys():
        if song_name in command:
            play_song(song_name)
            break
    else:
        st.write("Sorry, song not recognized. Please say the correct song name.")

# Example voice command function
def listen_for_music_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    st.write("Only say: 'song one or song two'")
    st.write("Listening for music commands...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            st.write(f"Command recognized: {command}")
            handle_music_command(command)
        except sr.UnknownValueError:
            st.write("Sorry, I didn't catch that.")
        except sr.RequestError as e:
            st.write(f"Could not request results from Google Speech Recognition service; {e}")

# Voice command button in Streamlit
if st.button("Start Music Voice Assistant"):
    listen_for_music_commands()
