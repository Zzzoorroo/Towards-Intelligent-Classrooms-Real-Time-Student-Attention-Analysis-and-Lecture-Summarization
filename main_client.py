import os 
import cv2
from src.modules.face_module import FaceHandler

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#silence tensor flow logging
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

handler = FaceHandler(path="data/face_db")
result = None
frame_count = 0
print("Looking for face...")

while result is None :
    ret,frame = cap.read()
    
    if not ret:
        print("Failed to grab a frame")
        break
    frame_count+=1
    if frame_count % 90 == 0:
        result = handler.is_authorized(frame)

cap.release()
cv2.destroyAllWindows()

if result:
    clean_name = os.path.splitext(result)[0]
    print(f"Access Granted: {clean_name}")