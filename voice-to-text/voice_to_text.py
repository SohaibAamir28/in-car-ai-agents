import streamlit as st
import sounddevice as sd
import numpy as np
import whisper
import soundfile as sf

# Set up Streamlit app
st.title("Real-time Voice-to-Text with Whisper")

# Whisper model loading
@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

# Record audio using sounddevice
def record_audio(duration=5, fs=16000):
    st.write(f"Recording for {duration} seconds...")
    recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
    sd.wait()  # Wait until recording is finished
    st.success("Recording finished.")
    return recording

# Save audio to file
def save_audio_file(audio_data, samplerate, filename="recorded_audio.wav"):
    sf.write(filename, audio_data, samplerate)
    return filename

# Record and display transcription
if st.button("Record and Transcribe"):
    # Record audio
    duration = st.slider("Select duration to record (seconds):", 1, 10, 5)
    audio_data = record_audio(duration)
    
    # Save the recorded audio as a file
    filename = save_audio_file(audio_data, 16000)
    
    # Load the audio and pad/trim it to fit 30 seconds
    audio = whisper.load_audio(filename)
    audio = whisper.pad_or_trim(audio)

    # Make log-Mel spectrogram and move to the same device as the model
    mel = whisper.log_mel_spectrogram(audio).to(model.device)

    # Detect the spoken language
    _, probs = model.detect_language(mel)
    st.write(f"Detected language: {max(probs, key=probs.get)}")

    # Decode the audio
    options = whisper.DecodingOptions()
    result = whisper.decode(model, mel, options)

    # Display the recognized text
    st.write("Transcription:")
    st.write(result.text)

    # Store the transcription in a file (optional)
    with open("transcription.txt", "w") as f:
        f.write(result.text)
    st.success("Transcription saved to 'transcription.txt'")
