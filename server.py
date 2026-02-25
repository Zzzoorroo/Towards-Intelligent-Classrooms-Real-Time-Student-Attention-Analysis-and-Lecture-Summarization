from flask import Flask, request, jsonify
from datetime import datetime
import json
import os 

app = Flask(__name__)

DB_FILE = "classroom_data.json"

def save_to_disk():
    with open(DB_FILE, "w") as f:
        json.dump(classroom_state, f, indent=4)

# In-memory storage for our real-time classroom data
classroom_state = {
    "lecture_summaries": [],
    "student_attention": []
}
# Use an absolute path or ensure it's in the script's directory
script_dir = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(script_dir, "classroom_data.json")

def load_from_disk():
    """Load existing data so we don't overwrite it on restart."""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️ Error loading DB: {e}")
    return {"lecture_summaries": [], "student_attention": []}

def save_to_disk():
    """Atomically save the state to a JSON file."""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(classroom_state, f, indent=4)
        # Optional: print confirm to console to be sure
        # print(f"💾 Data synced to {DB_FILE}") 
    except Exception as e:
        print(f"❌ Failed to save to disk: {e}")

# Initialize state by loading what's already there
classroom_state = load_from_disk()

@app.route('/api/summary', methods=['POST'])
def receive_summary():
    """Endpoint for the Teacher Client to send lecture transcripts/summaries."""
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Invalid data"}), 400
        
    entry = {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "text": data['text']
    }
    classroom_state["lecture_summaries"].append(entry)
    
    print(f"\n [SERVER] Received new lecture chunk ({len(data['text'])} chars)")
    save_to_disk()
    return jsonify({"status": "success"}), 200

@app.route('/api/attention', methods=['POST'])
def receive_attention():
    """Endpoint for the Student Client to send focus metrics."""
    data = request.json
    if not data:
        return jsonify({"error": "Invalid data"}), 400
        
    # Append timestamp
    data["timestamp"] = datetime.now().strftime("%H:%M:%S")
    classroom_state["student_attention"].append(data)
    
    print(f" [SERVER] Received attention update for {data.get('student_id', 'Unknown')}")
    save_to_disk()
    return jsonify({"status": "success"}), 200

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """Endpoint to view all collected data."""
    return jsonify(classroom_state), 200

if __name__ == '__main__':
    print(" Starting Central Classroom Server on http://127.0.0.1:5000")
    # debug=True allows the server to auto-reload if you change the code
    app.run(host='0.0.0.0', port=5000, debug=True)