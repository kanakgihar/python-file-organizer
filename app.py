from flask import Flask, render_template
import os

app = Flask(__name__)

WATCH_FOLDER = "test_files"


@app.route("/")
def home():

    stats = {
        "total_files": 0,
        "documents": 0,
        "videos": 0,
        "images": 0
    }

    for root, dirs, files in os.walk(WATCH_FOLDER):

        stats["total_files"] += len(files)

        if "Documents" in root:
            stats["documents"] += len(files)

        if "Videos" in root:
            stats["videos"] += len(files)

        if "Images" in root:
            stats["images"] += len(files)

    return render_template(
        "dashboard.html",
        stats=stats
    )


if __name__ == "__main__":
    app.run()