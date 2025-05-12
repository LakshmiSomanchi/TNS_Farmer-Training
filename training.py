import streamlit as st
import os
import json
import time
from pathlib import Path
import matplotlib.image as mpimg

# Set the Streamlit page configuration
st.set_page_config(page_title="TechnoServe Training Platform", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #042f5c; /* Background color for the sidebar */
        }

        [data-testid="stSidebar"] .css-qrbaxs {
            color: #ffffff; /* White text color for the sidebar */
            font-weight: bold;
        }

        /* Text Styling */
        body, div, h1, h2, h3, h4, h5, p, span, li {
            color: #000000 !important; /* Black text color for the main content */
            font-weight: bold !important;
        }

        /* Header Styling */
        .header {
            text-align: center;
            font-size: 40px;
            color: #556b2f; /* Dark olive green for headings */
            padding: 20px;
            background-color: #ffffff; /* White background for the header */
            border-radius: 10px;
        }

        /* Page Background */
        .stApp {
            background-color: #ffffff; /* White background for the main page */
        }
    </style>
""", unsafe_allow_html=True)

# Display the TechnoServe logo
logo_path = "TechnoServe_logo.png"  # Ensure the file is in the same directory
st.image(logo_path, caption="TechnoServe Logo", width=250)  # Adjust width if needed

# --- Sidebar: Program Selection ---
st.sidebar.header("🎓 Program Selection")
selected_program = st.sidebar.selectbox("🌟 Choose a Program", ["Cotton", "Dairy"])

# Update subcategories and folder path based on the selected program
if selected_program == "Cotton":
    SUBCATEGORIES = ["ppt", "video", "audio", "quiz"]
    MEDIA_FOLDER = "training_materials/cotton"
elif selected_program == "Dairy":
    SUBCATEGORIES = ["ppt", "video", "audio", "quiz"]
    MEDIA_FOLDER = "training_materials/dairy"

# --- Sidebar: Training Material Selection ---
st.sidebar.header("🔍 Navigation")
selected_category = st.sidebar.radio("📂 Select Training Material", SUBCATEGORIES)
folder_path = Path(MEDIA_FOLDER) / selected_category

# --- Header Animation ---
st.markdown(f"""
    <div class="header">
        🌾 Welcome to the TechnoServe Training Platform - {selected_program} Program 🌾
    </div>
""", unsafe_allow_html=True)

# --- Main Area ---
st.markdown(f"### 📚 {selected_program} - {selected_category.title()} Module")

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
            for file in files:
                if file.endswith(".mp4"):
                    st.video(str(folder_path / file))

        elif selected_category == "audio":
            for file in files:
                if file.endswith(".mp3"):
                    st.audio(str(folder_path / file))

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
                    st.progress(score / total)
                    st.success(f"🎉 Your Score: {score} / {total}")
            else:
                st.info("No quiz files found.")
