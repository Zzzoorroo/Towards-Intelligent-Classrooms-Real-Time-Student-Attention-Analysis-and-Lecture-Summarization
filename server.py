import os
import cv2
import base64
import json
from datetime import datetime
from flask import Flask, request, jsonify, render_template, redirect, url_for

# Import your custom modules
from src.modules.face_module import FaceHandler

app = Flask(__name__)

# --- CONFIGURATION ---
USER_DB = "users.json"
DB_FILE = "classroom_data.json"
FACE_DB_PATH = "data/face_db"
os.makedirs(FACE_DB_PATH, exist_ok=True)


def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f: return json.load(f)
    return {} # { "student_id": "password" }

def save_users(users):
    with open(USER_DB, "w") as f: json.dump(users, f, indent=4)

users_table = load_users()
# Initialize the FaceHandler once for the server
# This allows the server to verify logins via the web interface
print("🔄 Initializing Server FaceHandler (DeepFace)...")
handler = FaceHandler(path=FACE_DB_PATH)

# --- DATA PERSISTENCE ---
def load_from_disk():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return {"lecture_summaries": [], "student_attention": []}

def save_to_disk():
    with open(DB_FILE, "w") as f:
        json.dump(classroom_state, f, indent=4)

# Global state
classroom_state = load_from_disk()

# --- WEB PAGE ROUTES ---

@app.route('/')
def index():
    """Main entry point: Redirects to login."""
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    """The monitoring page (Gated by your login logic)."""
    return render_template('dashboard.html')

# --- AUTHENTICATION API ---

@app.route('/api/register', methods=['POST'])
def register_student():
    data = request.json
    student_id = data.get('student_id')
    password = data.get('password') # New field
    image_b64 = data.get('image')

    # 1. Save Password
    users = load_users()
    users[student_id] = password
    save_users(users)

    # 2. Save Face (Same logic as before)
    user_dir = os.path.join(FACE_DB_PATH, student_id)
    os.makedirs(user_dir, exist_ok=True)
    header, encoded = image_b64.split(",", 1)
    with open(os.path.join(user_dir, "registration.jpg"), "wb") as f:
        f.write(base64.b64decode(encoded))
    
    return jsonify({"message": "Account created!"}), 200

@app.route('/api/login', methods=['POST'])
def login_id_pw():
    data = request.json
    sid = data.get('student_id')
    pw = data.get('password')

    users = load_users()
    if sid in users and users[sid] == pw:
        return jsonify({"success": True, "redirect": "/dashboard"}), 200
    return jsonify({"success": False, "error": "Invalid Credentials"}), 401
# --- CLASSROOM DATA API ---

@app.route('/api/summary', methods=['POST'])
def receive_summary():
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid data"}), 400
        
    entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "text": data['text']
    }
    classroom_state["lecture_summaries"].append(entry)
    save_to_disk()
    return jsonify({"status": "success"}), 200

@app.route('/api/attention', methods=['POST'])
def receive_attention():
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
        
    data["timestamp"] = datetime.now().strftime("%H:%M:%S")
    classroom_state["student_attention"].append(data)
    save_to_disk()
    return jsonify({"status": "success"}), 200

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    return jsonify(classroom_state), 200

if __name__ == '__main__':
    print("🚀 Central Server running on http://127.0.0.1:5000")
    app.run(host='0.0.0.0', port=5000, debug=False) # debug=False to avoid multi-init of FaceHandler