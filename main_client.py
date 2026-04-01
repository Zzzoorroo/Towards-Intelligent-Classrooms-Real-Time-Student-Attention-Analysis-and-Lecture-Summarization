import requests
import datetime
import json
import os 
import cv2
from pynput import keyboard
from src.modules.face_module import FaceHandler
from src.modules.attention import AttentionTracker

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#silence tensor flow logging
print("Step 1: Initializing Camera...")
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

handler = FaceHandler(path="data/face_db")
result = None
frame_count = 0
print("Looking for face...")

# You can pass the student_id as an argument or have it ask
current_user_id = input("Please enter your Student ID to begin session: ")
print(f"Verifying identity for {current_user_id}...")

user_img_path = f"data/face_db/{current_user_id}/registration.jpg"
if not os.path.exists(user_img_path):
    print(f"Access Denied: No registration image found for student ID {current_user_id}")
    cap.release()
    cv2.destroyAllWindows()
    exit()

while result is None:
    ret, frame = cap.read()

    if not ret:
        break

    frame_count += 1
    if frame_count % 60 == 0:
        # Instead of 'is_authorized' (which finds anyone),
        # use a direct comparison against the specific folder
        # DeepFace verification logic
        try:
            from deepface import DeepFace
            v = DeepFace.verify(frame, user_img_path, enforce_detection=False)
            if v["verified"]:
                result = user_img_path
                clean_name = current_user_id
        except:
            pass

if result:
    clean_name = os.path.basename(os.path.dirname(result))
    print(f"Access Granted: {clean_name}")
    
    print("Initializing attention protocol...")
    tracker = AttentionTracker()
    
    stats = {"Focused": 0, "Distracted": 0, "Missing": 0, "Security_alert": 0}
    missing_streak = 0 

    try:
        while True:
            ret, frame = cap.read()
            
            if not ret:
                print("Failed to grab frame")
                break
            frame = cv2.flip(frame, 1)
            frame_count+=1
            if frame_count %30 == 0:
                metrics = tracker.get_attention_metrics(frame)

                #to be deleted 
                current_status = metrics.get('status', 'Unknown')
                
                if metrics['status'] == 'Focused':
                    stats["Focused"] = stats.get("Focused",0) + 1
                    missing_streak = 0 
                elif current_status == "No Face Detected": # Ensure this matches your tracker's exact output
                    missing_streak += 1
                    # Once we hit 5 consecutive strikes (approx 5 seconds), log it as missing
                    if missing_streak >= 5:
                        stats["Missing"] = stats.get("Missing",0) + 1
                        
                else:
                    # Captures 'Distracted' or any other unhandled status
                    stats["Distracted"] = stats.get("Distracted",0) + 1
                    missing_streak = 0
            if frame_count % 90 == 0:
                audit_result = handler.is_authorized(frame)
                if audit_result:
                    audit_name = os.path.basename(os.path.dirname(audit_result))
                    if audit_name == clean_name:
                        print(f"✅ Identity confirmed: {audit_name}")
                    if audit_name != clean_name:
                        print(f"WARNING: Identity mismatch! Expected {clean_name}, found {audit_name}")
                        stats["Security_alert"] = stats.get("Security_alert", 0) + 1
                else:
                    # Unauthorized access detected
                    print(f"🚨 SECURITY ALERT: Unauthorized person detected!")
                    stats["Security_alert"] = stats.get("Security_alert", 0) + 1
            #3 minute network push
                try:
                    live_url = "http://127.0.0.1:5000/api/attention"
                    # We send the current stats dictionary
                    requests.post(live_url, json={
                        "student_id": clean_name,
                        "Focused": stats["Focused"],
                        "Distracted": stats["Distracted"],
                        "Security_alert": stats["Security_alert"]
                    }, timeout=0.5)
                except:
                    pass
    except KeyboardInterrupt:
        print("\n🛑 Session ended by user.")
        
    # --- END OF SESSION BACKUP ---
    except Exception as e:
        print(f"⚠️ UNEXPECTED ERROR: {e}")
    finally:
        print(" Cleaning up hardware resources...")
    cap.release()
    cv2.destroyAllWindows()
    print(" Camera released safely.")
    
    print(stats)
    print(f"--- Session Summary for {clean_name} ---")
    print(f"Total Frames Processed: {frame_count}")
    total = sum(stats.values())
    if total>0:
        for key,value in stats.items():
            pct=(value/total)*100
            print(f"{key}: {pct:.2f}%")
    print("-------------------------------------")
    cap.release()
    cv2.destroyAllWindows()
else:
    print("Access Denied: No face recognized")
    cap.release()
    cv2.destroyAllWindows()
    #i will change the folder name from name into id but later on the data base that will be the primary key to etreive the needed info 

final_payload = {
    "student_id" : clean_name,
    "timestamp" : datetime.datetime.now().isoformat(),
    "session_start" : stats
}

server_url = "http://127.0.0.1:5000/api/attention"

print("Attempting to send report to the server....")


try:
    response = requests.post(server_url, json=final_payload, timeout=5)
    if response.status_code == 200:
        print("Sucess! Server received the data ")
    else:
        print(f"Server error: {response.status_code}")
except requests.exceptions.ConnectionError:
    print("Failed: Server is offline. Saving Backup locally...")
    clean_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"backup_report_{clean_time}.json"
    with open(filename,"w") as f:
        json.dump(final_payload, f, indent=4)
        print(f"Data saved succesfully saved to {filename}")
except requests.exceptions.Timeout:
    print("Failed: Server timed out.")
except Exception as e:
    print(f"An error has occured {e}")
