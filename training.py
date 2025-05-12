import streamlit as st
import os
from pathlib import Path
from pptx import Presentation
import time

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

# Directory for uploaded content
UPLOAD_DIR = "training_materials/admin_uploads"
Path(UPLOAD_DIR).mkdir(parents=True, exist_ok=True)

if is_admin:
    st.sidebar.header("⚙️ Admin Panel")
    st.sidebar.markdown("Welcome, Admin!")

    # Admin Feature 1: Upload Content
    st.header("📤 Upload Training Content")
    uploaded_file = st.file_uploader("Choose a file to upload (PDF, MP4, MP3, JSON, PPTX)", type=["pdf", "mp4", "mp3", "json", "pptx"])
    if uploaded_file:
        save_path = st.text_input("Enter the folder path to save the file:", UPLOAD_DIR)
        if st.button("Upload"):
            if not os.path.exists(save_path):
                os.makedirs(save_path)
            file_path = os.path.join(save_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success(f"File '{uploaded_file.name}' uploaded successfully to {save_path}!")
            if uploaded_file.name.endswith(".pptx"):
                st.info("Converting PPTX to PDF...")
                convert_ppt_to_pdf(file_path, save_path)
                st.success(f"PPTX file '{uploaded_file.name}' converted to PDF and saved in {save_path}!")

    # Admin Feature 2: View Uploaded Content
    st.header("📂 Manage Uploaded Content")
    uploaded_files = os.listdir(UPLOAD_DIR)
    if uploaded_files:
        st.markdown(f"**Uploaded Files in `{UPLOAD_DIR}`:**")
        for file in uploaded_files:
            file_path = os.path.join(UPLOAD_DIR, file)
            st.markdown(f"- {file}")
            if st.button(f"Delete {file}", key=file):
                os.remove(file_path)
                st.warning(f"{file} has been deleted.")
    else:
        st.info("No uploaded content available.")

else:
    # Display the TechnoServe logo
    logo_path = "TechnoServe_logo.png"  # Ensure the file is in the same directory
    st.image(logo_path, caption="Empowering Farmers Worldwide", width=250)

    # Sidebar and user functionality goes here...
    st.warning("This section is only accessible to admin users.")
    
# Function to convert PPTX to PDF (simplified placeholder)
def convert_ppt_to_pdf(pptx_path, save_dir):
    pdf_file_path = os.path.join(save_dir, Path(pptx_path).stem + ".pdf")
    # Placeholder: Add actual conversion logic here (e.g., using external tools like LibreOffice)
    with open(pdf_file_path, "w") as f:
        f.write(f"Converted content of {pptx_path}")
    st.info(f"Converted PDF saved at {pdf_file_path}")
