import streamlit as st
import os
import json
import time
from pathlib import Path

# Config
st.set_page_config(page_title="Training Platform", layout="wide")
PROGRAMS = ["cotton", "dairy"]
SUBCATEGORIES = ["ppt", "video", "audio", "quiz"]
MEDIA_FOLDER = "training_materials"

# --- Header Animation ---
with st.container():
    st.markdown("""
        <style>
            .header {
                text-align: center;
                color: #4CAF50;
                font-size: 36px;
                margin-bottom: 10px;
                animation: fadeIn 2s;
            }
            .intro {
                text-align: center;
                font-size: 18px;
                color: #555;
                animation: fadeIn 2s;
            }
            .logo {
                display: block;
                margin: 0 auto;
                width: 200px; /* Adjust logo size */
                animation: bounce 2s infinite;
            }
            .program-panel {
                border: 2px solid #4CAF50;
                border-radius: 10px;
                padding: 20px;
                margin: 10px;
                text-align: center;
                background-color: #f9f9f9;
                transition: transform 0.2s, box-shadow 0.2s;
                animation: slideIn 0.5s forwards;
                opacity: 0;
            }
            .program-panel:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                40% { transform: translateY(-20px); }
                60% { transform: translateY(-10px); }
            }
            @keyframes slideIn {
                from { transform: translateY(20px); opacity: 0; }
                to { transform: translateY(0); opacity: 1; }
            }
        </style>
        <img src="https://upload.wikimedia.org/wikipedia/en/thumb/4/4e/TechnoServe_logo.svg/1200px-TechnoServe_logo.svg.png" class="logo" alt="Technoserve Logo">
        <h1 class="header">🌾 Welcome to the Interactive Training Platform 🌾</h1>
        <p class="intro">This training module is designed for farmers to enhance their skills and knowledge. Choose your program and training module to get started!</p>
    """, unsafe_allow_html=True)
    time.sleep(0.5)

# --- Sidebar ---
st.sidebar.header("🔍 Navigation")
selected_program = st.sidebar.selectbox("📘 Select Program", PROGRAMS)
selected_category = st.sidebar.radio("📂 Select Category", SUBCATEGORIES)
folder_path = Path(MEDIA_FOLDER) / selected_program / selected_category

# --- Main Area ---
st.markdown(f"### 📚 {selected_program.title()} - {selected_category.title()} Module")

if not folder_path.exists():
    st.warning("No content found for this category.")
else:
    files = os.listdir(folder_path)
    if not files:
        st.info("No files available.")
    else:
        if selected_category == "ppt":
            ppt_files = [f for f in files if f.endswith(".pdf")]
            if ppt_files:
                selected_ppt = st.selectbox("📑 Select a PPT file:", ppt_files)
                ppt_path = folder_path / selected_ppt
                with open(ppt_path, "rb") as f:
                    st.download_button(label=f"⬇️ Download {selected_ppt}", file_name=selected_ppt, data=f)
            else:
                st.info("No PPT files found.")

        elif selected_category == "video":
            video_files = [f for f in files if f.endswith(".mp4")]
            if video_files:
                selected_video = st.selectbox("🎥 Select a Video:", video_files)
                st.video(str(folder_path / selected_video))
            else:
                st.info("No video files found.")

        elif selected_category == "audio":
            audio_files = [f for f in files if f.endswith(".mp3")]
            if audio_files:
                selected_audio = st.selectbox("🎵 Select an Audio File:", audio_files)
                st.audio(str(folder_path / selected_audio))
            else:
                st.info("No audio files found.")

        elif selected_category == "quiz":
            quiz_files = [f for f in files if f.endswith(".json")]
            if quiz_files:
                selected_quiz = st.selectbox("📝 Choose a quiz:", quiz_files)
                quiz_path = folder_path / selected_quiz
                with open(quiz_path, "r") as f:
                    quiz = json.load(f)
                    st.subheader(quiz.get("title", "Quiz"))
                    score = 0
                    total = len(quiz["questions"])
                    for i, q in enumerate(quiz["questions"]):
                        st.markdown(f"**Q{i+1}. {q['question']}**")
                        selected = st.radio("Select an answer:", q['options'], key=f"q{i}")
                        if selected == q['answer']:
                            score += 1
                    st.success(f"🎉 Your Score: {score} / {total}")
            else:
                st.info("No quiz files found.")

# --- Add Animated Farmers ---
st.markdown("""
    <div style='text-align: center;'>
        <img src='https://media.giphy.com/media/3o7buirY1g1g1g1g1g/giphy.gif' alt='Animated Farmers' width='300'>
    </div>
""", unsafe_allow_html=True)
