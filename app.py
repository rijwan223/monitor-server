from flask import Flask, request, jsonify
import os, json
from datetime import datetime

app = Flask(__name__)

DATA_FOLDER = "data"
os.makedirs(DATA_FOLDER, exist_ok=True)

def save_data(file_name, data):
    path = os.path.join(DATA_FOLDER, file_name)
    with open(path, 'a') as f:
        f.write(json.dumps(data) + "\n")

@app.route('/upload/app-usage', methods=['POST'])
def upload_app_usage():
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    save_data('app_usage.json', data)
    return jsonify({"status": "success"})

@app.route('/upload/gps', methods=['POST'])
def upload_gps():
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    save_data('gps_logs.json', data)
    return jsonify({"status": "success"})

@app.route('/upload/screenshot', methods=['POST'])
def upload_screenshot():
    file = request.files.get('screenshot')
    if file:
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        file.save(os.path.join(DATA_FOLDER, filename))
        return jsonify({"status": "success", "filename": filename})
    return jsonify({"status": "error", "message": "No file uploaded"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
