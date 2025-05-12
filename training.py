import streamlit as st
import os
from pathlib import Path

# Set the Streamlit page configuration
st.set_page_config(page_title="TechnoServe Training Platform", layout="wide")

# Define the base directory for training materials
BASE_DIR = "training_materials"
PROGRAMS = ["Cotton", "Dairy"]
CATEGORIES = ["Presentations", "Videos", "Audios", "Quizzes"]

# Ensure the directory structure exists
for program in PROGRAMS:
    for category in CATEGORIES:
        Path(f"{BASE_DIR}/{program.lower()}/{category.lower()}").mkdir(parents=True, exist_ok=True)

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

if is_admin:
    st.sidebar.header("⚙️ Admin Panel")
    st.sidebar.markdown("Welcome, Admin!")

    # Admin Feature: Upload Content
    st.header("📤 Upload Training Content")
    selected_program = st.selectbox("🌟 Select Program", PROGRAMS)
    selected_category = st.selectbox("📂 Select Category", CATEGORIES)
    uploaded_file = st.file_uploader("Choose a file to upload", type=["pdf", "mp4", "mp3", "json", "pptx"])

    if uploaded_file:
        save_dir = f"{BASE_DIR}/{selected_program.lower()}/{selected_category.lower()}"
        Path(save_dir).mkdir(parents=True, exist_ok=True)
        file_path = os.path.join(save_dir, uploaded_file.name)

        if st.button("Upload"):
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File '{uploaded_file.name}' uploaded successfully to {save_dir}!")

else:
    # Display the TechnoServe logo
    logo_path = "TechnoServe_logo.png"  # Ensure the file is in the same directory
    st.image(logo_path, caption="Empowering Farmers Worldwide", width=250)

    # --- Sidebar: Program Selection ---
    st.sidebar.header("🎓 Program Selection")
    selected_program = st.sidebar.selectbox("🌟 Choose a Program", PROGRAMS)

    # --- Sidebar: Training Material Selection ---
    st.sidebar.header("🔍 Navigation")
    selected_category = st.sidebar.radio("📂 Select Training Material", CATEGORIES)

    # Display Header
    st.markdown(f"### 📚 {selected_program} - {selected_category} Module")

    # Get the folder path for the selected program and category
    folder_path = Path(BASE_DIR) / selected_program.lower() / selected_category.lower()

    # Check if the folder exists and display its contents
    if not folder_path.exists() or not any(folder_path.iterdir()):
        st.warning(f"No content available for the **{selected_category}** category in the {selected_program} program.")
    else:
        files = os.listdir(folder_path)
        for file in files:
            file_path = folder_path / file
            if file.endswith(".pdf"):
                st.markdown(f"📄 **{file}**")
                with open(file_path, "rb") as f:
                    st.download_button(label=f"⬇️ Download {file}", data=f, file_name=file)
            elif file.endswith(".mp4"):
                st.markdown(f"🎥 **{file}**")
                st.video(str(file_path))
            elif file.endswith(".mp3"):
                st.markdown(f"🎵 **{file}**")
                st.audio(str(file_path))
            elif file.endswith(".json"):
                st.markdown(f"📝 **{file}** (Quiz File)")
                with open(file_path, "r") as f:
                    st.json(json.load(f))
            elif file.endswith(".pptx"):
                st.markdown(f"📑 **{file} (PPTX)**")
                with open(file_path, "rb") as f:
                    st.download_button(label=f"⬇️ Download {file}", data=f, file_name=file)
