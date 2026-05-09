%%writefile app.py

import streamlit as st
import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Smart File Organizer Pro", layout="wide")

st.title("📂 Smart File Organizer Pro")

folder_path = st.text_input("Enter Folder Path")

image_ext = [".jpg", ".png", ".jpeg"]
doc_ext = [".pdf", ".txt", ".docx"]
video_ext = [".mp4", ".mkv"]
music_ext = [".mp3", ".wav"]
code_ext = [".py", ".html", ".cpp"]

if st.button("Organize Files"):

    if os.path.exists(folder_path):

        files = os.listdir(folder_path)

        file_data = []

        for file in files:

            file_path = os.path.join(folder_path, file)

            if os.path.isfile(file_path):

                ext = os.path.splitext(file)[1].lower()

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

                target_folder = os.path.join(folder_path, folder)

                os.makedirs(target_folder, exist_ok=True)

                shutil.move(file_path, os.path.join(target_folder, file))

                size = round(os.path.getsize(os.path.join(target_folder, file))/1024, 2)

                file_data.append([file, folder, size])

        st.success("✅ Files Organized Successfully!")

        df = pd.DataFrame(file_data, columns=["File Name", "Category", "Size (KB)"])

        st.subheader("📋 Organized Files")
        st.dataframe(df)

        category_count = df["Category"].value_counts()

        st.subheader("📊 File Distribution")

        fig, ax = plt.subplots()

        ax.pie(category_count, labels=category_count.index, autopct='%1.1f%%')

        st.pyplot(fig)

    else:
        st.error("❌ Invalid Folder Path")
