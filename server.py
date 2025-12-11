import os
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify

app = Flask(__name__)
if not os.path.exists("uploads"):
    os.makedirs("uploads")

upload_folder = "uploads"

def condb():
    conn = sqlite3.connect("fortify.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS intrusion_events(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            device_id TEXT,
            event_timestamp TEXT,
            image_filepath TEXT,
            status TEXT
        )
    """)
    conn.commit()
    conn.close()

condb()

@app.route("/api/upload", methods=["POST"])
def upload():

    device_id = request.form.get("device_id", "UNKNOWN_DEVICE")

    file = request.files.get("image")
    if file is None:
        return jsonify({"error": "No image uploaded"}), 400

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"capture_{timestamp}.jpg"
    file_path = os.path.join(upload_folder, filename)

    file.save(file_path)

    conn = sqlite3.connect("fortify.db")
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO intrusion_events(device_id, event_timestamp, image_filepath, status)
        VALUES (?, ?, ?, ?)
    """, (device_id, timestamp, file_path, "PENDING"))
    conn.commit()
    conn.close()

    return jsonify({
        "message": "Upload successful",
        "saved_as": filename
    }), 200


@app.route("/")
def home():
    return "Backend running successfully!"

if __name__ == "__main__":
    app.run()

