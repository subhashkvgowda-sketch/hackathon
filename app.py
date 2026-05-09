import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart File Organizer Pro", layout="wide")

st.title("📂 Smart File Organizer Pro")

uploaded_files = st.file_uploader(
    "Upload Files",
    accept_multiple_files=True
)

image_ext = [".jpg", ".png", ".jpeg"]
doc_ext = [".pdf", ".txt", ".docx"]
video_ext = [".mp4", ".mkv"]
music_ext = [".mp3", ".wav"]
code_ext = [".py", ".html", ".cpp"]

if st.button("Organize Files"):

    if uploaded_files:

        folders = ["Images", "Documents", "Videos", "Music", "Code", "Others"]

        for folder in folders:
            os.makedirs(folder, exist_ok=True)

        file_data = []

        for uploaded_file in uploaded_files:

            file_name = uploaded_file.name

            ext = os.path.splitext(file_name)[1].lower()

            if ext in image_ext:
                folder = "Images"

            elif ext in doc_ext:
                folder = "Documents"

            elif ext in video_ext:
                folder = "Videos"

            elif ext in music_ext:
                folder = "Music"

            elif ext in code_ext:
                folder = "Code"

            else:
                folder = "Others"

            save_path = os.path.join(folder, file_name)

            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())

            size = round(os.path.getsize(save_path)/1024, 2)

            file_data.append([file_name, folder, size])

        st.success("✅ Files Organized Successfully!")

        df = pd.DataFrame(
            file_data,
            columns=["File Name", "Category", "Size (KB)"]
        )

        st.subheader("📋 Organized Files")
        st.dataframe(df)

        category_count = df["Category"].value_counts()

        st.subheader("📊 File Distribution")

        fig, ax = plt.subplots()

        ax.pie(
            category_count,
            labels=category_count.index,
            autopct='%1.1f%%'
        )

        st.pyplot(fig)

    else:
        st.warning("Please upload files")
    else:
        st.warning("Please upload files")
