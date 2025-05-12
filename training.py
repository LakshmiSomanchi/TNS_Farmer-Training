# training.py
import streamlit as st
import os
import json

PROGRAMS = ["cotton", "dairy"]
SUBCATEGORIES = ["ppt", "video", "audio", "quiz"]
MEDIA_FOLDER = "training_materials"

st.sidebar.title("Program Selector")
selected_program = st.sidebar.selectbox("Choose a Program", PROGRAMS)
selected_category = st.sidebar.radio("Choose Category", SUBCATEGORIES)

folder_path = os.path.join(MEDIA_FOLDER, selected_program, selected_category)

st.title(f"Training Platform - {selected_program.title()} - {selected_category.title()}")

if not os.path.exists(folder_path):
    st.warning("No content found for this category.")
else:
    files = os.listdir(folder_path)
    if not files:
        st.info("No files available.")
    for file in files:
        file_path = os.path.join(folder_path, file)

        if selected_category == "video" and file.endswith(".mp4"):
            st.video(file_path)

        elif selected_category == "audio" and file.endswith(".mp3"):
            st.audio(file_path)

        elif selected_category == "ppt" and file.endswith(".pdf"):
            with open(file_path, "rb") as f:
                st.download_button(label=file, file_name=file, data=f)

        elif selected_category == "quiz" and file.endswith(".json"):
            with open(file_path, "r") as f:
                quiz = json.load(f)
                st.subheader(quiz.get("title", "Quiz"))
                score = 0
                total = len(quiz["questions"])
                for i, q in enumerate(quiz["questions"]):
                    st.markdown(f"**Q{i+1}. {q['question']}**")
                    selected = st.radio("Select an answer:", q['options'], key=f"q{i}")
                    if selected == q['answer']:
                        score += 1
                st.success(f"Your Score: {score} / {total}")
