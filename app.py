import streamlit as st
import os
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Smart File Organizer Pro",
    layout="wide"
)

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

organized_files = {
    "Images": [],
    "Documents": [],
    "Videos": [],
    "Music": [],
    "Code": [],
    "Others": []
}

if st.button("Organize Files"):

    if uploaded_files:

        file_data = []

        for uploaded_file in uploaded_files:

            file_name = uploaded_file.name

            ext = os.path.splitext(file_name)[1].lower()

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

            size = round(len(uploaded_file.getbuffer()) / 1024, 2)

            organized_files[category].append(uploaded_file)

            file_data.append([file_name, category, size])

        st.success("✅ Files Organized Successfully!")

        df = pd.DataFrame(
            file_data,
            columns=["File Name", "Category", "Size (KB)"]
        )

        st.subheader("📋 Organized Files")
        st.dataframe(df)

        # Search
        search = st.text_input("🔍 Search File")

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

                st.markdown(f"## {category}")

                for file in files:

                    st.write(f"📄 {file.name}")

                    # Image Preview
                    if category == "Images":
                        st.image(file, width=200)

                    # Download Button
                    st.download_button(
                        label=f"⬇ Download {file.name}",
                        data=file,
                        file_name=file.name
                    )

    else:

        st.warning("Please upload files")
