import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import hashlib
import qrcode
from io import BytesIO

# PAGE SETTINGS
st.set_page_config(
    page_title="Smart File Organizer Pro AI",
    layout="wide"
)

st.title("📂 Smart File Organizer Pro AI")

# FILE UPLOAD
uploaded_files = st.file_uploader(
    "Upload Files",
    accept_multiple_files=True
)

# FILE TYPES
image_ext = [".jpg", ".png", ".jpeg"]
doc_ext = [".pdf", ".txt", ".docx"]
video_ext = [".mp4", ".mkv"]
music_ext = [".mp3", ".wav"]
code_ext = [".py", ".html", ".cpp"]

# ORGANIZED FILE STORAGE
organized_files = {
    "Images": [],
    "Documents": [],
    "Videos": [],
    "Music": [],
    "Code": [],
    "Others": []
}

# DUPLICATE DETECTION FUNCTION
def get_file_hash(file_path):

    hasher = hashlib.md5()

    with open(file_path, "rb") as f:
        buffer = f.read()
        hasher.update(buffer)

    return hasher.hexdigest()


# MAIN BUTTON
if st.button("Organize Files"):

    if uploaded_files:

        # CREATE FOLDERS
        for folder in organized_files.keys():
            os.makedirs(folder, exist_ok=True)

        file_data = []

        # PROCESS FILES
        for uploaded_file in uploaded_files:

            file_name = uploaded_file.name

            ext = os.path.splitext(file_name)[1].lower()

            # FILE CATEGORY
            if ext in image_ext:
                category = "Images"

            elif ext in doc_ext:
                category = "Documents"

            elif ext in video_ext:
                category = "Videos"

            elif ext in music_ext:
                category = "Music"

            elif ext in code_ext:
                category = "Code"

            else:
                category = "Others"

            # SAVE FILE
            save_path = os.path.join(category, file_name)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            organized_files[category].append(save_path)

            size = round(os.path.getsize(save_path) / 1024, 2)

            file_data.append([file_name, category, size])

        # SUCCESS MESSAGE
        st.success("✅ Files Organized Successfully!")

        # DATAFRAME
        df = pd.DataFrame(
            file_data,
            columns=["File Name", "Category", "Size (KB)"]
        )

        st.subheader("📋 Organized Files")
        st.dataframe(df)

        # SEARCH FEATURE
        search = st.text_input("🔍 Search File")

        if search:

            filtered_df = df[
                df["File Name"].str.contains(search, case=False)
            ]

            st.dataframe(filtered_df)

        # PIE CHART
        st.subheader
