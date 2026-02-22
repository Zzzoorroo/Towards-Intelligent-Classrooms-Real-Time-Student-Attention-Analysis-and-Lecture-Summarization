from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# In-memory storage for our real-time classroom data
classroom_state = {
    "lecture_summaries": [],
    "student_attention": []
}

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
    return jsonify({"status": "success"}), 200

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard_data():
    """Endpoint to view all collected data."""
    return jsonify(classroom_state), 200

if __name__ == '__main__':
    print(" Starting Central Classroom Server on http://127.0.0.1:5000")
    # debug=True allows the server to auto-reload if you change the code
    app.run(host='0.0.0.0', port=5000, debug=True)