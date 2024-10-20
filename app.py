import streamlit as st
import speechrecognition as sr
from together import Together
import time

# Set page config
st.set_page_config(page_title="Car Infotainment System", layout="wide")

# Custom styles
st.markdown("""
    <style>
    .title-text {
        font-size: 36px;
        font-weight: bold;
        color: white;
        text-align: center;
        background-color: #008cba;
        padding: 10px;
        border-radius: 5px;
    }
    .section {
        padding: 15px;
        border-radius: 10px;
        background-color: #333;
        margin-bottom: 20px;
    }
    .temperature {
        font-size: 50px;
        font-weight: bold;
        color: #00aced;
        text-align: center;
    }
    .destination-label {
        font-size: 18px;
        color: white;
    }
    .button-blue {
        background-color: #008cba;
        color: white;
        padding: 10px 20px;
        border-radius: 10px;
        text-align: center;
        margin-top: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# Page title
st.markdown('<div class="title-text">Car Infotainment System</div>', unsafe_allow_html=True)

# Layout: Three columns
col1, col2 = st.columns([1, 1])

# Initialize the Together client
@st.cache_resource
def get_together_client():
    return Together(api_key='97d77defec520871d1e2d66980d1b37c350065417d8e3ca9f331c20a145bd9b2')  # Replace with your Together API key

client = get_together_client()

# Function to process commands using Llama
def process_command(query, model="meta-llama/Llama-3.2-3B-Instruct-Turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful AI assistant for controlling car systems like AC, Music, and Navigation."},
            {"role": "user", "content": query}
        ],
        max_tokens=100,
        temperature=0.7
    )
    return response.choices[0].message.content

# Temperature control variables
current_temp = 22

# AC Control section
with col1:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("🌡️ AC Control")
    st.text("Temperature:")
    st.markdown(f'<div class="temperature">{current_temp}°C</div>', unsafe_allow_html=True)
    
    # Temperature adjustment buttons
    col_a1, col_a2, col_a3 = st.columns([3, 1, 1])
    with col_a2:
        if st.button("➖"):
            current_temp -= 1
    with col_a3:
        if st.button("➕"):
            current_temp += 1
    st.markdown("</div>", unsafe_allow_html=True)

# Music Player section
with col2:
    st.markdown('<div class="section">', unsafe_allow_html=True)
    st.subheader("🎵 Music Player")
    st.text("Now Playing:")
    st.text("Song Title - Artist")
    
    # Music control buttons
    col_b1, col_b2, col_b3 = st.columns([1, 1, 1])
    with col_b1:
        st.button("⏮️")
    with col_b2:
        st.button("⏯️")
    with col_b3:
        st.button("⏭️")
    st.markdown("</div>", unsafe_allow_html=True)

# Maps section
st.markdown('<div class="section">', unsafe_allow_html=True)
st.subheader("📍 Maps")
st.markdown('<label class="destination-label">Destination:</label>', unsafe_allow_html=True)
destination = st.text_input("Enter destination")
if st.button("Get Directions"):
    st.markdown('<div class="button-blue">Fetching Directions...</div>', unsafe_allow_html=True)

# Footer
st.markdown('<div style="text-align: center; color: white; font-size: 14px;">@ in-car-ai-agent | lablab.ai | 2024</div>', unsafe_allow_html=True)
st.markdown('<div style="text-align: center; color: black; font-size: 14px;">edge-runners-3-point-2 hackathon</div>', unsafe_allow_html=True)

# Voice command function
def listen_for_commands():
    recognizer = sr.Recognizer()
    mic = sr.Microphone()
    
    st.write("Listening for voice commands...")

    with mic as source:
        recognizer.adjust_for_ambient_noise(source)

        while True:
            try:
                print("Listening...")
                audio = recognizer.listen(source)
                command = recognizer.recognize_google(audio)
                
                st.write(f"Command recognized: {command}")
                handle_command(command)
                
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")

# Handle recognized voice command
def handle_command(command):
    st.write(f"Processing command: {command}")
    
    # Use Llama model to understand the command
    response = process_command(command)
    
    # Execute the response or action
    global current_temp  # Make sure to modify the global variable
    if "temperature" in command:
        if "set to" in command:
            # Extract the temperature value
            temp_value = int(command.split("set to")[1].strip().replace("°C", ""))
            current_temp = temp_value
            st.write(f"Temperature set to {current_temp}°C.")
        elif "increase" in command:
            current_temp += 1
            st.write(f"Temperature increased to {current_temp}°C.")
        elif "decrease" in command:
            current_temp -= 1
            st.write(f"Temperature decreased to {current_temp}°C.")
    
    elif "play" in command or "pause" in command:
        st.write("Music command received.")
    
    elif "directions" in command:
        st.write("Fetching directions...")

# Run voice command listening in a separate thread
if st.button("Start Voice Assistant"):
    listen_for_commands()



# ---------------------------------------------------

# voice

# import streamlit as st
# import speech_recognition as sr
# import openai

# # Function to get voice commands
# def get_voice_command():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         st.write("Listening for your command...")
#         audio = recognizer.listen(source)
#         try:
#             voice_input = recognizer.recognize_google(audio)
#             st.write(f"Voice Command: {voice_input}")
#             return voice_input
#         except sr.UnknownValueError:
#             st.write("Sorry, I did not understand that.")
#             return None

# # Process the command using LLaMA or OpenAI
# def process_command(command):
#     response = openai.Completion.create(
#         engine="meta-llama/Llama-3.2-3B-Instruct-Turbo",  # Replace with LLaMA 3.2 or similar
#         prompt=f"Car command: {command}. Interpret and suggest actions.",
#         max_tokens=50
#     )
#     return response.choices[0].text.strip()

# # Streamlit app layout
# st.title("Car Infotainment Dashboard")

# # Sidebar to switch between modules
# module = st.sidebar.selectbox("Select Module", ["AC Control", "Music Player", "Maps Control"])

# # Execute based on module selection
# if module == "AC Control":
#     st.header("AC Control")
#     st.write("Adjust temperature and fan speed")
#     voice_command = get_voice_command()
#     if voice_command:
#         action = process_command(voice_command)
#         st.write(f"Executing AC Control: {action}")

# elif module == "Music Player":
#     st.header("Music Player")
#     st.write("Control music playback")
#     voice_command = get_voice_command()
#     if voice_command:
#         action = process_command(voice_command)
#         st.write(f"Executing Music Player Control: {action}")

# elif module == "Maps Control":
#     st.header("Maps Control")
#     st.write("Manage navigation and set destinations")
#     voice_command = get_voice_command()
#     if voice_command:
#         action = process_command(voice_command)
#         st.write(f"Executing Maps Control: {action}")
