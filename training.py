import streamlit as st
import os
import json
import time
from pathlib import Path
import random

# Set the Streamlit page configuration
st.set_page_config(page_title="TechnoServe Training Platform", layout="wide")

# Custom CSS for enhanced styling and pop-ups
st.markdown("""
    <style>
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #2e3b4e; /* Dark Slate Blue */
        }

        [data-testid="stSidebar"] .css-qrbaxs {
            color: #f1f1f1; /* Light Gray for Sidebar Text */
            font-weight: bold;
            font-size: 16px;
        }

        /* Text Styling */
        body, div, h1, h2, h3, h4, h5, p, span, li {
            color: #333333 !important; /* Dark Gray for Main Content Text */
            font-family: 'Arial', sans-serif !important; /* Clean Font */
            line-height: 1.6;
        }

        /* Header Styling */
        .header {
            text-align: center;
            font-size: 42px;
            color: #1e5128; /* Forest Green for Header Text */
            padding: 20px;
            background-color: #f7f7f7; /* Off-White Background for Header */
            border-radius: 15px;
            border: 2px solid #1e5128;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
        }

        /* Buttons */
        .stButton>button {
            background-color: #1e5128; /* Forest Green for Buttons */
            color: #ffffff; /* White Text */
            border-radius: 8px;
            font-size: 16px;
            padding: 10px 20px;
            border: none;
            transition: background-color 0.3s ease;
        }
        .stButton>button:hover {
            background-color: #144d2f; /* Darker Green on Hover */
        }

        /* Pop-up for Achievements */
        .popup {
            position: fixed;
            bottom: 10%;
            right: 10%;
            background-color: #f1c40f; /* Golden Yellow */
            color: #000;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);
            font-family: 'Arial', sans-serif;
            font-size: 16px;
        }

        /* Page Background */
        .stApp {
            background-color: #f0f4f8; /* Light Grayish Blue for Background */
        }

        /* Links */
        a {
            color: #1e5128; /* Forest Green for Links */
            font-weight: bold;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Display the TechnoServe logo
logo_path = "TechnoServe_logo.png"  # Ensure the file is in the same directory
st.image(logo_path, caption="Empowering Farmers Worldwide", width=250)

# --- Sidebar: Gamified Progress and Program Selection ---
st.sidebar.header("🎓 Program Selection")
selected_program = st.sidebar.selectbox("🌟 Choose a Program", ["Cotton", "Dairy"])

# Progress tracker
if "progress" not in st.session_state:
    st.session_state.progress = 0

if "badge" not in st.session_state:
    st.session_state.badge = None

# Update subcategories and folder path based on the selected program
if selected_program == "Cotton":
    SUBCATEGORIES = ["Presentations", "Videos", "Audios", "Quizzes"]
    MEDIA_FOLDER = "training_materials/cotton"
elif selected_program == "Dairy":
    SUBCATEGORIES = ["Presentations", "Videos", "Audios", "Quizzes"]
    MEDIA_FOLDER = "training_materials/dairy"

# --- Sidebar: Training Material Selection ---
st.sidebar.header("🔍 Navigation")
selected_category = st.sidebar.radio("📂 Select Training Material", SUBCATEGORIES)
folder_path = Path(MEDIA_FOLDER) / selected_category.lower()

# --- Header Animation ---
st.markdown(f"""
    <div class="header">
        🌾 Welcome to the TechnoServe Training Platform - {selected_program} Program 🌾
    </div>
""", unsafe_allow_html=True)

# --- Main Area ---
st.markdown(f"### 📚 {selected_program} - {selected_category} Module")

# Gamified pop-up achievement
if st.session_state.badge:
    st.markdown(f"""
        <div class="popup">
            🎉 Congratulations! You've earned the **{st.session_state.badge}** badge!
        </div>
    """, unsafe_allow_html=True)
    time.sleep(3)  # Simulate pop-up display time
    st.session_state.badge = None

if not folder_path.exists():
    st.warning(f"No content found for the **{selected_category}** category.")
else:
    files = os.listdir(folder_path)
    if not files:
        st.info(f"No files available in the **{selected_category}** category.")
    else:
        if selected_category == "Presentations":
            ppt_files = [f for f in files if f.endswith(".pdf")]
            if ppt_files:
                selected_ppt = st.selectbox("📑 Select a Presentation:", ppt_files)
                ppt_path = folder_path / selected_ppt
                with open(ppt_path, "rb") as f:
                    st.download_button(label=f"⬇️ Download {selected_ppt}", file_name=selected_ppt, data=f)
                st.session_state.progress += 10
            else:
                st.info("No Presentation files found.")

        elif selected_category == "Videos":
            for file in files:
                if file.endswith(".mp4"):
                    st.video(str(folder_path / file))
                    st.session_state.progress += 10

        elif selected_category == "Audios":
            for file in files:
                if file.endswith(".mp3"):
                    st.audio(str(folder_path / file))
                    st.session_state.progress += 10

        elif selected_category == "Quizzes":
            quiz_files = [f for f in files if f.endswith(".json")]
            if quiz_files:
                selected_quiz = st.selectbox("📝 Choose a Quiz:", quiz_files)
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
                    st.progress(score / total)
                    st.success(f"🎉 Your Score: {score} / {total}")
                    st.session_state.progress += score * 5
                    if score / total > 0.8:
                        st.session_state.badge = "Quiz Master"
            else:
                st.info("No quiz files found.")

# Display progress bar
st.sidebar.markdown("### 🏆 Your Progress")
st.sidebar.progress(st.session_state.progress)

# Display badges earned
if st.session_state.progress >= 50:
    st.sidebar.success("🎖 You’ve unlocked the **Intermediate Farmer** badge!")
if st.session_state.progress >= 100:
    st.sidebar.success("🎖 You’ve unlocked the **Master Farmer** badge!")
