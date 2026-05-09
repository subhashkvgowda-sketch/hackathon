import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import hashlib
import qrcode
from io import BytesIO

st.set_page_config(
    page_title="Smart File Organizer Pro AI",
    layout="wide"
)

st.title("📂 Smart File Organizer Pro AI")

uploaded_files = st.file_uploader(
    "Upload Files",
    accept_multiple_files=True
)

image_ext = [".jpg", ".png", ".jpeg"]
doc_ext = [".pdf", ".txt", ".docx"]
video_ext = [".mp4", ".mkv"]
music_ext = [".mp3", ".wav"]
code_ext = [".py", ".html", ".cpp"]

organized_files = {
    "Images": [],
    "Documents": [],
    "Videos": [],
    "Music": [],
    "Code": [],
    "Others": []
}

# Duplicate Detection Function
def get_file_hash(file_path):

    hasher = hashlib.md5()

    with open(file_path, "rb") as f:
        buffer = f.read()
        hasher.update(buffer)

    return hasher.hexdigest()


if st.button("Organize Files"):

    if uploaded_files:

        folders = list(organized_files.keys())

        for folder in folders:
            os.makedirs(folder, exist_ok=True)

        file_data = []

        for uploaded_file in uploaded_files:

            file_name = uploaded_file.name

            ext = os.path.splitext(file_name)[1].lower()

            # Categorization
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

            save_path = os.path.join(category, file_name)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            organized_files[category].append(save_path)

            size = round(os.path.getsize(save_path) / 1024, 2)

            file_data.append([file_name, category, size])

        st.success("✅ Files Organized Successfully!")

        df = pd.DataFrame(
            file_data,
            columns=["File Name", "Category", "Size (KB)"]
        )

        st.subheader("📋 Organized Files")
        st.dataframe(df)

        # Search Feature
        search = st.text_input("🔍 Search File")

        if search:

            filtered_df = df[
                df["File Name"].str.contains(search, case=False)
            ]

            st.dataframe(filtered_df)

        # Pie Chart
        st.subheader("📊 File Distribution")
