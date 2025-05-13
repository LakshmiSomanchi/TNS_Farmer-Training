import streamlit as st
import os
from pathlib import Path
import json

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

# Custom CSS for agriculture theme
st.markdown("""
    <style>
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #D1F5D4; /* Green for nature */
        }
        [data-testid="stSidebar"] .css-qrbaxs {
            color: #ffffff; /* White text for sidebar */
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
        /* Links */
        a {
            color: #4caf50; /* Green for links */
            font-weight: bold;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Admin Authentication with Session State
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False  # Initialize admin state

def admin_login():
    """Admin login for restricted access."""
    if st.session_state.is_admin:
        st.sidebar.success("✅ You are logged in as Admin.")
        return True

    st.sidebar.subheader("🔒 Admin Login")
    admin_username = st.sidebar.text_input("Admin Username", type="default", key="admin_username")
    admin_password = st.sidebar.text_input("Admin Password", type="password", key="admin_password")
    if st.sidebar.button("Login"):
        if admin_username == "admin" and admin_password == "admin123":
            st.sidebar.success("✅ Login Successful!")
            st.session_state.is_admin = True
            return True
        else:
            st.sidebar.error("❌ Invalid credentials. Please try again.")
    return False

# File type validation based on category
def is_valid_file(file_name, category):
    valid_extensions = {
        "Presentations": [".pptx"],
        "Videos": [".mp4"],
        "Audios": [".mp3"],
        "Quizzes": [".xlsx", ".png", ".jpg", ".jpeg"]
    }
    # Allow Excel and Images in all categories
    extra_extensions = [".xlsx", ".png", ".jpg", ".jpeg"]
    file_extension = os.path.splitext(file_name)[1].lower()

    if file_extension in extra_extensions:
        return True
    if category in valid_extensions and file_extension in valid_extensions[category]:
        return True
    return False

# Check if the user is an admin
is_admin = admin_login()

if is_admin:
    st.sidebar.header("⚙️ Admin Panel")
    st.sidebar.markdown("Welcome, Admin!")

    # --- Admin Feature: Upload Content ---
    st.header("📤 Upload Training Content")
    selected_program = st.selectbox("🌟 Select Program", PROGRAMS, key="program_dropdown")
    selected_category = st.selectbox("📂 Select Category", CATEGORIES, key="category_dropdown")
    uploaded_file = st.file_uploader("Choose a file to upload", type=["pdf", "mp4", "mp3", "json", "pptx", "xlsx", "png", "jpg", "jpeg"])

    if uploaded_file:
        save_dir = f"{BASE_DIR}/{selected_program.lower()}/{selected_category.lower()}"
        Path(save_dir).mkdir(parents=True, exist_ok=True)  # Ensure directory exists
        file_path = os.path.join(save_dir, uploaded_file.name)

        # Validate file type
        if not is_valid_file(uploaded_file.name, selected_category):
            st.error(f"❌ Invalid file type for the **{selected_category}** category.")
        else:
            if st.button("Upload"):
                try:
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    st.success(f"✅ File '{uploaded_file.name}' uploaded successfully to {save_dir}!")
                except Exception as e:
                    st.error(f"❌ Error uploading file: {e}")

    # --- Admin Feature: Delete Content ---
    st.header("🗑️ Delete Training Content")
    delete_program = st.selectbox("🗂️ Select Program to View Files", PROGRAMS, key="delete_program_dropdown")
    delete_category = st.selectbox("📂 Select Category to View Files", CATEGORIES, key="delete_category_dropdown")
    delete_folder_path = Path(BASE_DIR) / delete_program.lower() / delete_category.lower()

    if delete_folder_path.exists() and any(delete_folder_path.iterdir()):
        delete_files = os.listdir(delete_folder_path)
        delete_file = st.selectbox("🗑️ Select a File to Delete", delete_files, key="delete_file_dropdown")

        if st.button("Delete File"):
            try:
                os.remove(delete_folder_path / delete_file)
                st.success(f"✅ File '{delete_file}' has been deleted!")
            except Exception as e:
                st.error(f"❌ Error deleting file: {e}")
    else:
        st.warning(f"No files available in the **{delete_category}** category of the {delete_program} program.")

else:
    st.warning("You must be an admin to upload or delete training materials.")

# --- Main Content ---
# Add a Gamified Header for the Main Page
st.markdown("""
<div class="header">
    🌾 <span style="font-weight: bold;">Farmer Training Program</span> 🌾
</div>
""", unsafe_allow_html=True)

# Add Interactive Gamification Elements
st.markdown("### 🎮 Level Up Your Farming Skills!")
st.markdown("""
    <p>Welcome to the Farmer Training Program! Complete tasks, learn new skills, and earn rewards to become a <b>Master Farmer</b>.</p>
    <ul>
        <li>📚 Access training materials</li>
        <li>🎯 Complete quizzes</li>
        <li>🏆 Earn badges</li>
    </ul>
""", unsafe_allow_html=True)

# Add a Button for a Gamified Start
if st.button("🌟 Start Your Journey"):
    st.success("🎉 You're on your way to becoming a Master Farmer! Explore the training materials below.")

selected_program = st.sidebar.selectbox("🌟 Choose a Program", PROGRAMS, key="view_program_dropdown")
selected_category = st.sidebar.radio("📂 Select Training Material", CATEGORIES, key="view_category_radio")

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
        elif file.endswith((".png", ".jpg", ".jpeg")):
            st.markdown(f"🖼️ **{file}**")
            st.image(str(file_path))
        elif file.endswith(".pptx"):
            st.markdown(f"📑 **{file} (PPTX)**")
            with open(file_path, "rb") as f:
                st.download_button(label=f"⬇️ Download {file}", data=f, file_name=file)
