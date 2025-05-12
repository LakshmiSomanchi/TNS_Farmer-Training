# training.py
import streamlit as st
import os
import json
import time
from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load the TechnoServe logo
logo_path = "TechnoServe_logo.png"  # Ensure the file is in the same directory or update the path accordingly
img = mpimg.imread(TechnoServe_logo.png)

# Display the logo
plt.imshow(img)
plt.axis('off')  # Hide axes
plt.title("TechnoServe Logo")  # Optional title
plt.show()
# Config
st.set_page_config(page_title="Training Platform", layout="wide")
PROGRAMS = ["cotton", "dairy"]
SUBCATEGORIES = ["ppt", "video", "audio", "quiz"]
MEDIA_FOLDER = "training_materials"

# --- Header Animation ---
with st.container():
    st.markdown("""
        <h1 style='text-align: center; color: #4CAF50;'>🌾 Welcome to the Interactive Training Platform 🌾</h1>
        <p style='text-align: center; font-size: 18px;'>Choose your program and training module to get started!</p>
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
                    st.success(f"🎉 Your Score: {score} / {total}")
            else:
                st.info("No quiz files found.")
