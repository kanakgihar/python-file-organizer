import os
import shutil
from datetime import datetime
from smart_sorter import analyze_pdf

# ===== CONFIGURATION =====
SOURCE_FOLDER = "test_files"

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".txt", ".docx"],
    "Videos": [".mp4", ".mkv"],
    "Music": [".mp3"],
    "Archives": [".zip", ".rar"]
}

LOG_FILE = "automation_log.txt"


# ===== WRITE LOG =====
def write_log(message):

    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")


# ===== CREATE FOLDER =====
def create_folder(folder_path):

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

        write_log(f"Created folder: {folder_path}")


# ===== RENAME FILE =====
def generate_new_name(file):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    return f"{timestamp}_{file}"


# ===== MAIN FUNCTION =====
def organize_files():

    try:

        if not os.path.exists(SOURCE_FOLDER):

            print("Source folder not found.")
            return

        files = os.listdir(SOURCE_FOLDER)

        if not files:

            print("No files found.")
            return

        for file in files:

            file_path = os.path.join(SOURCE_FOLDER, file)

            # Skip folders
            if os.path.isdir(file_path):
                continue

            _, extension = os.path.splitext(file)

            moved = False

            # ===== SMART PDF SORTING =====
            if extension.lower() == ".pdf":

                category = analyze_pdf(file_path)

                category_folder = os.path.join(
                    SOURCE_FOLDER,
                    category
                )

                create_folder(category_folder)

                new_filename = generate_new_name(file)

                destination = os.path.join(
                    category_folder,
                    new_filename
                )

                shutil.move(file_path, destination)

                print(f"Smart Sorted PDF: {file} → {category}")

                write_log(
                    f"Smart sorted PDF '{file}' into '{category}'"
                )

                continue

            # ===== NORMAL SORTING =====
            for category, extensions in FILE_CATEGORIES.items():

                if extension.lower() in extensions:

                    category_folder = os.path.join(
                        SOURCE_FOLDER,
                        category
                    )

                    create_folder(category_folder)

                    new_filename = generate_new_name(file)

                    destination = os.path.join(
                        category_folder,
                        new_filename
                    )

                    # Prevent duplicates
                    if os.path.exists(destination):

                        print(f"Duplicate skipped: {file}")

                        write_log(f"Duplicate skipped: {file}")

                        moved = True
                        break

                    shutil.move(file_path, destination)

                    print(
                        f"Moved: {file} → {category}/{new_filename}"
                    )

                    write_log(
                        f"Moved '{file}' to '{category}'"
                    )

                    moved = True
                    break

            # ===== UNKNOWN FILES =====
            if not moved:

                other_folder = os.path.join(
                    SOURCE_FOLDER,
                    "Others"
                )

                create_folder(other_folder)

                destination = os.path.join(
                    other_folder,
                    generate_new_name(file)
                )

                shutil.move(file_path, destination)

                print(f"Moved unknown file: {file}")

                write_log(
                    f"Unknown file moved: {file}"
                )

    except PermissionError:

        print("Permission denied.")

        write_log("ERROR: Permission denied.")

    except FileNotFoundError:

        print("File not found.")

        write_log("ERROR: File not found.")

    except Exception as e:

        print(f"Unexpected Error: {e}")

        write_log(f"ERROR: {e}")


# ===== RUN =====
if __name__ == "__main__":

    organize_files()