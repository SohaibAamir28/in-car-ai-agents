import streamlit as st
from st_audiorec import st_audiorec
import whisper
from transformers import AutoTokenizer, AutoModelForCausalLM
import pyttsx3

# Initialize Whisper model for transcription
@st.cache_resource
def load_whisper_model():
    return whisper.load_model("base")

whisper_model = load_whisper_model()

# Initialize LLaMA model
@st.cache_resource
def load_llama_model():
    tokenizer = AutoTokenizer.from_pretrained("facebook/llama-7b-hf")  # Adjust the model size as needed
    model = AutoModelForCausalLM.from_pretrained("facebook/llama-7b-hf")  # Adjust the model size as needed
    return tokenizer, model

tokenizer, llama_model = load_llama_model()

# Initialize text-to-speech engine (using pyttsx3)
def text_to_speech(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Transcribe audio using Whisper
def transcribe_audio_whisper(audio_data):
    # Save audio to a file temporarily
    with open("temp.wav", "wb") as f:
        f.write(audio_data)

    # Transcribe the audio file using Whisper
    audio = whisper.load_audio("temp.wav")
    audio = whisper.pad_or_trim(audio)
    transcription = whisper_model.transcribe(audio)
    return transcription['text']

# Generate a response using LLaMA
def generate_llama_response(input_text):
    inputs = tokenizer(input_text, return_tensors="pt")
    outputs = llama_model.generate(inputs.input_ids, max_length=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

# Main Streamlit app
def main():
    st.sidebar.title("LLaMA & Whisper Offline Voice Assistant")
    st.title("Learn Language by Speaking with LLaMA")
    st.write("Click on the microphone to interact.")

    # Record audio from microphone
    recorded_audio = st_audiorec()

    if 'messages' not in st.session_state:
        st.session_state['messages'] = []

    if recorded_audio:
        # Transcribe the audio
        transcribed_text = transcribe_audio_whisper(recorded_audio)
        st.write("Transcribed Text: ", transcribed_text)

        # Update conversation history
        st.session_state['messages'].append({"role": "user", "content": transcribed_text})

        # Get AI response using LLaMA
        ai_response = generate_llama_response(transcribed_text)
        st.session_state['messages'].append({"role": "assistant", "content": ai_response})

        # Display AI response
        st.write("AI Response: ", ai_response)

        # Convert AI response to speech and play it
        text_to_speech(ai_response)

if __name__ == "__main__":
    main()
