import streamlit as st
import os
import json
import time
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Set the Streamlit page configuration
st.set_page_config(page_title="TechnoServe Training Platform", layout="wide")

# Display the TechnoServe logo
logo_path = "TechnoServe_logo.png"  # Ensure the file is in the same directory
st.image(logo_path, caption="TechnoServe Logo", width=250)  # Adjust width if needed

# Config
PROGRAMS = ["cotton", "dairy"]
SUBCATEGORIES = ["ppt", "video", "audio", "quiz"]
MEDIA_FOLDER = "training_materials"

# Add a loading spinner
with st.spinner("Loading..."):
    time.sleep(2)  # Simulate loading time
st.success("Content loaded successfully!")

# --- Header Animation ---
st.markdown("""
    <style>
        .header {
            text-align: center;
            font-size: 40px;
            color: #4CAF50;
            padding: 20px;
            background-color: #f9f9f9;
            border-radius: 10px;
        }
    </style>
    <div class="header">
        🌾 Welcome to the TechnoServe Training Platform 🌾
    </div>
""", unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("🔍 Navigation")
selected_program = st.sidebar.selectbox("📘 Select Training Program", PROGRAMS)
selected_category = st.sidebar.radio("📂 Select Training Material", SUBCATEGORIES)
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
                    st.progress(score / total)
                    st.success(f"🎉 Your Score: {score} / {total}")
            else:
                st.info("No quiz files found.")

# --- Example Chart ---
st.markdown("### 📊 Example Interactive Chart")
data = px.data.gapminder()
fig = px.scatter(data, x="gdpPercap", y="lifeExp", color="continent", 
                 size="pop", hover_name="country", log_x=True, size_max=60)
st.plotly_chart(fig)

# --- Program Highlights ---
st.markdown("### 🌟 Training Programs")
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div style="text-align: center;">
            <h3>📘 Cotton Program</h3>
            <p>Learn about best practices in cotton farming.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Select Cotton Program", key="cotton"):
        st.success("Cotton Program selected!")

with col2:
    st.markdown("""
        <div style="text-align: center;">
            <h3>📘 Dairy Program</h3>
            <p>Explore techniques for improving dairy production.</p>
        </div>
    """, unsafe_allow_html=True)
    if st.button("Select Dairy Program", key="dairy"):
        st.success("Dairy Program selected!")

# --- Styling and Background ---
st.markdown("""
    <style>
        body {
            background-color: #fefefe;
        }
        h1, h2, h3 {
            color: #4CAF50;
        }
    </style>
""", unsafe_allow_html=True)
