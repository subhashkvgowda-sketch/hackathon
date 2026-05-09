import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt
import zipfile
import hashlib
import qrcode
from io import BytesIO

# Page Configuration
st.set_page_config(
    page_title="Smart File Organizer Pro AI",
    layout="wide"
)

st.title("📂 Smart File Organizer Pro AI")

st.markdown("### Upload files and organize them intelligently")

# Upload Files
uploaded_files = st.file_uploader(
    "📤 Upload Files",
    accept_multiple_files=True
)

# File Extensions
image_ext = [".jpg", ".png", ".jpeg"]
doc_ext = [".pdf", ".txt", ".docx"]
video_ext = [".mp4", ".mkv"]
music_ext = [".mp3", ".wav"]
code_ext = [".py", ".html", ".cpp"]

# Organized File Dictionary
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


# Main Button
if st.button("🚀 Organize Files"):

    if uploaded_files:

        # Create folders
        folders = list(organized_files.keys())

        for folder in folders:
            os.makedirs(folder, exist_ok=True)

        file_data = []

        # Process uploaded files
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

            # Save files
            save_path = os.path.join(category, file_name)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            organized_files[category].append(save_path)

            # File Size
            size = round(os.path.getsize(save_path) / 1024, 2)

            file_data.append([file_name, category, size])

        st.success("✅ Files Organized Successfully!")

        # Dataframe
        df = pd.DataFrame(
            file_data,
            columns=["File Name", "Category", "Size (KB)"]
        )

        st.subheader("📋 Organized Files")

        st.dataframe(df)

        # Search Feature
        st.subheader("🔍 Search Files")

        search = st.text_input("Enter file name")

        if search:

            filtered_df = df[
                df["File Name"].str.contains(search, case=False)
            ]

            st.dataframe(filtered_df)

        # Pie Chart
        st.subheader("📊 File Distribution")

        category_count = df["Category"].value_counts()

        fig, ax = plt.subplots()

        ax.pie(
            category_count,
            labels=category_count.index,
            autopct='%1.1f%%'
        )

        st.pyplot(fig)

        # Segregated Files
        st.subheader("📁 Segregated Files")

        for category, files in organized_files.items():

            if files:

                st.markdown(f"## 📂 {category}")

                for file_path in files:

                    file_name = os.path.basename(file_path)

                    st.write(f"📄 {file_name}")

                    # Image Preview
                    if category == "Images":
                        st.image(file_path, width=250)

                    # Individual Download Button
                    with open(file_path, "rb") as f:

                        st.download
