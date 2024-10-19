import io
import base64
import streamlit as st
import os
from together import Together
from PIL import Image
import requests
from io import BytesIO

# Set page config
st.set_page_config(page_title="In-Car AI Agents", page_icon="🚗", layout="wide")

# Custom CSS to improve the app's appearance
st.markdown("""
    <style>
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    .st-bw {
        background-color: #f0f2f6;
    }
    .stButton>button {
        width: 100%;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize the Together client
# Initialize the Together client without relying on st.secrets
@st.cache_resource
def get_together_client():
    return Together(api_key='97d77defec520871d1e2d66980d1b37c350065417d8e3ca9f331c20a145bd9b2')

client = get_together_client()


def process_text_query(query, model="meta-llama/Llama-3.2-3B-Instruct-Turbo"):
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant for in-car navigation and driver assistance tasks."},
            {"role": "user", "content": query}
        ],
        max_tokens=300,
        temperature=0.7
    )
    return response.choices[0].message.content

def process_image_query(image_base64, query, model="meta-llama/Llama-3.2-90B-Vision-Instruct-Turbo"):
    system_message = f"You are an expert AI assistant analyzing in-car camera images for navigation and assistance. Analyze {image_base64} and provide detailed insights for the driver."

    example_analysis = """
Example analysis for a road image:
1. Road Conditions: Wet pavement observed; caution advised.
2. Traffic: Moderate congestion ahead; suggest alternative route.
3. Obstacles: Identify pedestrians and cyclists; advise slowing down.
4. Navigation: Suggest best route to destination considering real-time traffic.
    """

    structured_query = f"""
Analyze the provided {image_base64} and address the following points:
1. Describe key features in the image, including road signs, obstacles, and traffic.
2. Provide real-time navigation suggestions based on the analysis.
3. Identify any potential hazards or points of interest.
4. Suggest improvements for safe driving based on the current image.
5. Provide 2-3 actionable next steps for the driver based on your analysis.

{query}

Remember to base your analysis solely on what you can see in the image, and provide specific, detailed insights relevant to in-car navigation and assistance.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": "Here's an example of the kind of analysis I'm looking for:" + example_analysis},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": structured_query},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_base64}"}}
                ]
            },
        ],
        max_tokens=500,
        temperature=0.7
    )
    return response.choices[0].message.content

def image_to_base64(image):
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode('utf-8')

# Sidebar
with st.sidebar:
    st.title("In-Car AI Agents")
    st.info("This AI-powered assistant helps with navigation, safety, and entertainment while driving.")
    st.markdown("---")
    st.write("Powered by Llama 3.2 models")

# Main content
st.title("Welcome to Your In-Car AI Assistant")

task_type = st.radio("Select Task Type", ["Text Query", "Image Analysis"])

if task_type == "Text Query":
    st.header("Text Query")
    query = st.text_input("Enter your query:")
    if st.button("Process Query", key="text_query"):
        if query:
            with st.spinner("Processing..."):
                response = process_text_query(query)
            st.success("Query processed successfully!")
            st.subheader("Response:")
            st.write(response)
        else:
            st.warning("Please enter a query.")

elif task_type == "Image Analysis":
    st.header("Image Analysis")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        query = st.text_input("Enter your analysis query:")
        if st.button("Analyze Image", key="image_analysis"):
            if query:
                with st.spinner("Analyzing image..."):
                    # Convert image to base64
                    image_base64 = image_to_base64(image)
                    
                    # Process image query
                    response = process_image_query(image_base64, query)
                st.success("Image analyzed successfully!")
                st.subheader("Analysis:")
                st.write(response)
            else:
                st.warning("Please enter an analysis query.")
    else:
        st.info("Please upload an image to analyze.")

# Footer
st.markdown("---")
st.markdown("🚗 Your In-Car AI Assistant")
