import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

# Load environment variables
load_dotenv()

# Configure Gemini with your API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt template
prompt = """
You are an AI assistant specialized in summarizing YouTube videos. 
Your task is to analyze the provided transcript text and generate a concise summary that highlights the most important points and takeaways from the video. 
Keep the summary well-structured, informative, and limited to approximately 250 words. Please provide the summary of the text given here:
"""

# Get transcript from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("v=")[-1].split("&")[0]  # More robust parsing
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)
        transcript = " ".join([i["text"] for i in transcript_text])
        return transcript
    except Exception as e:
        raise Exception("Failed to retrieve transcript. Make sure the video has subtitles.") from e

# Generate summary from transcript using Gemini
def generate_gemini_content(transcript_text, prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        print (response.text)
    except Exception as e:
        raise Exception("Gemini API error: " + str(e))

# Streamlit UI
st.title("YouTube Transcript to Detailed Notes Converter")
youtube_link = st.text_input("Enter YouTube Video Link here...")

if youtube_link:
    try:
        video_id = youtube_link.split("v=")[-1].split("&")[0]
        st.image(f"https://img.youtube.com/vi/{video_id}/0.jpg", use_container_width=True)
    except:
        st.warning("Could not load thumbnail.")

if st.button("Get Detailed Notes"):
    if youtube_link:
        try:
            transcript_text = extract_transcript_details(youtube_link)
            if transcript_text:
                summary = generate_gemini_content(transcript_text, prompt)
                st.markdown("## 📝 Detailed Notes")
                st.write(summary)
        except Exception as e:
            st.error(str(e))
    else:
        st.warning("Please enter a valid YouTube link.")
