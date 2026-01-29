import os 
import cv2
from pynput import keyboard
from src.modules.face_module import FaceHandler
from src.modules.attention import AttentionTracker

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#silence tensor flow logging
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

handler = FaceHandler(path="data/face_db")
result = None
frame_count = 0
print("Looking for face...")

while result is None:
    ret, frame = cap.read()
    
    if not ret:
        print("Failed to grab a frame")
        break
    frame_count+=1
    if frame_count % 90 == 0:
        result = handler.is_authorized(frame)

if result:
    clean_name = os.path.basename(os.path.dirname(result))
    print(f"Access Granted: {clean_name}")
    
    print("Initializing attention protocol...")
    tracker = AttentionTracker()
    
    stats = {"Focused": 0, "Distracted": 0, "Missing": 0}

    while True:
        ret, frame = cap.read()
        
        if not ret:
            print("Failed to grab frame")
            break
        frame = cv2.flip(frame, 1)
        frame_count+=1
        if frame_count %30 == 0:
            metrics = tracker.get_attention_metrics(frame)
            if metrics['status'] == 'Focused':
                stats["Focused"] = stats.get("Focused",0) + 1
            elif metrics['status'] == "No Face Detected":
                stats["Missing"] = stats.get("Missing",0) + 1
            else:
                stats["Distracted"] = stats.get("Distracted",0) + 1
        
        cv2.imshow('Tracker Feed', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("User requested exit. Closing...")
            break
    
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