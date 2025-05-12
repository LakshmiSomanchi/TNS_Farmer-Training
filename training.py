import streamlit as st
import os
import json
import time
from pathlib import Path

# Set the Streamlit page configuration
st.set_page_config(page_title="TechnoServe Training Platform", layout="wide")

# Admin Authentication
def admin_login():
    """Admin login for restricted access."""
    st.sidebar.subheader("🔒 Admin Login")
    admin_username = st.sidebar.text_input("Admin Username", type="default")
    admin_password = st.sidebar.text_input("Admin Password", type="password")
    if st.sidebar.button("Login"):
        if admin_username == "admin" and admin_password == "admin123":
            st.sidebar.success("✅ Login Successful!")
            return True
        else:
            st.sidebar.error("❌ Invalid credentials. Please try again.")
    return False

# Check if the user is an admin
is_admin = admin_login()

# If admin logged in, show admin panel
if is_admin:
    st.sidebar.header("⚙️ Admin Panel")
    st.sidebar.markdown("Welcome, Admin!")

    # Admin Feature 1: Upload Content
    st.header("📤 Upload Training Content")
    uploaded_file = st.file_uploader("Choose a file to upload", type=["pdf", "mp4", "mp3", "json"])
    if uploaded_file:
        save_path = st.text_input("Enter the folder path to save the file:", "training_materials/admin_uploads")
        if st.button("Upload"):
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            with open(os.path.join(save_path, uploaded_file.name), "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File '{uploaded_file.name}' uploaded successfully to {save_path}!")

    # Admin Feature 2: Monitor Real-Time Activities
    st.header("📊 Real-Time Monitoring")
    st.markdown("Here you can track real-time activities of trainers and participants.")
    if "progress" in st.session_state:
        st.markdown(f"**Platform Progress**: {st.session_state.progress}%")
    else:
        st.markdown("No progress data available.")

    # Add more admin functionalities here
    st.header("🔧 Additional Admin Tools")
    st.markdown("These tools are for advanced admin functionalities (e.g., analytics, user management).")

# If not admin, show training platform
else:
    # Display the TechnoServe logo
    logo_path = "TechnoServe_logo.png"  # Ensure the file is in the same directory
    st.image(logo_path, caption="Empowering Farmers Worldwide", width=250)

    # --- Agriculture and Dairy Theme ---
    st.markdown("""
        <style>
            /* Sidebar Styling */
            [data-testid="stSidebar"] {
                background-color: #8FBC8F; /* Earthy Green */
            }

            [data-testid="stSidebar"] .css-qrbaxs {
                color: #FFFFFF; /* White text for sidebar */
                font-weight: bold;
                font-size: 16px;
            }

            /* Header Styling */
            .header {
                text-align: center;
                font-size: 42px;
                color: #6B4226; /* Soil Brown */
                padding: 20px;
                background-color: #EEE8AA; /* Wheat Color */
                border-radius: 15px;
                border: 2px solid #6B4226;
                box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
            }

            /* Page Background */
            .stApp {
                background-color: #F5F5DC; /* Beige for natural tones */
            }
        </style>
    """, unsafe_allow_html=True)

    # --- Sidebar: Program Selection ---
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
