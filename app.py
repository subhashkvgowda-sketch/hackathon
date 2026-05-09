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

st.write("Upload files to organize, detect duplicates, and download ZIP folders.")

# FILE UPLOAD
uploaded_files = st.file_uploader(
    "📤 Upload Files",
    accept_multiple_files=True
)

# FILE EXTENSIONS
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
if st.button("🚀 Organize Files"):

    if uploaded_files:

        # CREATE FOLDERS
        folders = list(organized_files.keys())

        for folder in folders:
            os.makedirs(folder, exist_ok=True)

        file_data = []

        # PROCESS FILES
        for uploaded_file in uploaded_files:

            file_name = uploaded_file.name

            ext = os.path.splitext(file_name)[1].lower()

            # CATEGORIZATION
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

            # FILE SIZE
            size = round(os.path.getsize(save_path) / 1024, 2)

            file_data.append([file_name, category, size])

        st.success("✅ Files Organized Successfully!")

        # DATAFRAME
        df = pd.DataFrame(
            file_data,
            columns=["File Name", "Category", "Size (KB)"]
        )

        st.subheader("📋 Organized Files")
        st.dataframe(df)

        # SEARCH FEATURE
        st.subheader("🔍 Search Files")

        search = st.text_input("Enter file name")

        if search:

            filtered_df = df[
                df["File Name"].str.contains(search, case=False)
            ]

            st.dataframe(filtered_df)

        # PIE CHART
        st.subheader("📊 File Distribution")

        category_count = df["Category"].value_counts()

        fig, ax = plt.subplots()

        ax.pie(
            category_count,
            labels=category_count.index,
            autopct='%1.1f%%'
        )

        st.pyplot(fig)

        # SEGREGATED FILES
        st.subheader("📁 Segregated Files")

        for category, files in organized_files.items():

            if files:

                st.markdown(f"## {category}")

                for file_path in files:

                    file_name = os.path.basename(file_path)

                    st.write(f"📄 {file_name}")

                    # IMAGE PREVIEW
                    if category == "Images":
                        st.image(file_path, width=200)

                    # DOWNLOAD BUTTON
                    with open(file_path, "rb") as f:

                        st.download_button(
                            label=f"⬇ Download {file_name}",
                            data=f,
                            file_name=file_name
                        )

        # DUPLICATE FILE DETECTION
        st.subheader("🛑 Duplicate File Detection")

        hashes = {}

        duplicates = []

        for category, files in organized_files.items():

            for file_path in files:

                file_hash = get_file_hash(file_path)

                if file_hash in hashes:

                    duplicates.append(file_path)

                else:

                    hashes[file_hash] = file_path

        if duplicates:

            st.error("⚠ Duplicate Files Found!")

            for dup in duplicates:

                st.write("📄", os.path.basename(dup))

        else:

            st.success("✅ No Duplicate Files Found")

        # CREATE ZIP FILE
        zip_filename = "Organized_Files.zip"

        with zipfile.ZipFile(zip_filename, "w") as zipf:

            for category, files in organized_files.items():

                for file_path in files:

                    zipf.write(file_path)

        # ZIP DOWNLOAD BUTTON
        st.subheader("📦 Download Complete ZIP Folder")

        with open(zip_filename, "rb") as f:

            st.download_button(
                label="⬇ Download ZIP Folder",
                data=f,
                file_name=zip_filename,
                mime="application/zip"
            )

        # QR CODE GENERATION
        st.subheader("📱 QR Code Generator")

        app_url = st.text_input("Enter Your Streamlit App URL")

        if app_url:

            qr = qrcode.make(app_url)

            buf = BytesIO()

            qr.save(buf)

            st.image(buf)

    else:

        st.warning("⚠ Please upload files")
