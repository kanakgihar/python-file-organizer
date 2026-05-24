import os
import shutil
from datetime import datetime

# ===== CONFIGURATION =====
SOURCE_FOLDER = "test_files"

# File type categories
FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "Documents": [".pdf", ".docx", ".txt"],
    "Videos": [".mp4", ".mkv"],
    "Music": [".mp3"],
    "Archives": [".zip", ".rar"]
}

LOG_FILE = "automation_log.txt"


# ===== FUNCTION TO WRITE LOGS =====
def write_log(message):
    with open(LOG_FILE, "a") as log:
        log.write(f"{datetime.now()} - {message}\n")


# ===== FUNCTION TO CREATE FOLDERS =====
def create_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        write_log(f"Created folder: {folder_path}")


# ===== MAIN AUTOMATION FUNCTION =====
def organize_files():
    try:
        # Check if source folder exists
        if not os.path.exists(SOURCE_FOLDER):
            print("Source folder does not exist.")
            return

        # Read all files
        files = os.listdir(SOURCE_FOLDER)

        if not files:
            print("No files found in the folder.")
            return

        for file in files:
            file_path = os.path.join(SOURCE_FOLDER, file)

            # Skip folders
            if os.path.isdir(file_path):
                continue

            # Get file extension
            _, extension = os.path.splitext(file)

            moved = False

            # Sort files into categories
            for category, extensions in FILE_CATEGORIES.items():
                if extension.lower() in extensions:

                    category_folder = os.path.join(SOURCE_FOLDER, category)
                    create_folder(category_folder)

                    # Rename file with timestamp
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    new_filename = f"{timestamp}_{file}"

                    destination = os.path.join(category_folder, new_filename)

                    # Move + rename file
                    shutil.move(file_path, destination)

                    print(f"Moved: {file} → {category}/{new_filename}")

                    write_log(
                        f"Moved file '{file}' to '{category}' as '{new_filename}'"
                    )

                    moved = True
                    break

            # Files with unknown extensions
            if not moved:
                other_folder = os.path.join(SOURCE_FOLDER, "Others")
                create_folder(other_folder)

                destination = os.path.join(other_folder, file)
                shutil.move(file_path, destination)

                print(f"Moved unknown file: {file} → Others")

                write_log(f"Moved unknown file '{file}' to Others")

    except PermissionError:
        print("Permission denied while accessing files.")
        write_log("ERROR: Permission denied.")

    except FileNotFoundError:
        print("File not found.")
        write_log("ERROR: File not found.")

    except Exception as e:
        print(f"Unexpected Error: {e}")
        write_log(f"ERROR: {e}")


# ===== RUN SCRIPT =====
if __name__ == "__main__":
    organize_files()