import zipfile
import hashlib
def get_file_hash(file_path):

    hasher = hashlib.md5()

    with open(file_path, "rb") as f:

        buffer = f.read()

        hasher.update(buffer)

    return hasher.hexdigest()
    t.subheader("🛑 Duplicate File Detection")

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

            st.error("Duplicate Files Found!")

            for dup in duplicates:

                st.write("📄", os.path.basename(dup))

        else:

            st.success("✅ No Duplicate Files Found")
