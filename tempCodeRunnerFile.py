import os 
import cv2
from src.modules.face_module import FaceHandler

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#silence tensor flow logging
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

ret,frame = cap.read()    
handler = FaceHandler(path="data/face_db")
result = handler.is_authorized(frame)
while result == None:
    handler.is_authorized(frame)