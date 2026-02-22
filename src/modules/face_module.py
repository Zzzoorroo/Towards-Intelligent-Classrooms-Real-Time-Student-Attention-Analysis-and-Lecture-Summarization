from deepface import DeepFace
import cv2
import mediapipe as mp
import numpy as np
import os

class FaceHandler:
    def __init__(self, path):
        self.db_path = path
        self.current_user = None

    def is_authorized(self, frame):
        try:
            import os
            
            # 1. Extract all faces (enforce_detection=False prevents crashes if no face is detected)
            faces = DeepFace.extract_faces(img_path=frame, enforce_detection=False)
            
            # DeepFace returns a list of dictionaries. 
            # Filter out false positives by requiring a minimum confidence score.
            valid_faces = [f for f in faces if f.get('confidence', 0) > 0.5]
            
            if not valid_faces:
                return None
                
            # 2. Find the largest face by calculating area (width * height)
            largest_face = max(valid_faces, key=lambda f: f['facial_area']['w'] * f['facial_area']['h'])
            
            # 3. Get coordinates and crop the frame
            area = largest_face['facial_area']
            x, y, w, h = area['x'], area['y'], area['w'], area['h']
            
            # Add a slight 10px padding so the AI model has facial edge context
            y1 = max(0, y - 10)
            y2 = min(frame.shape[0], y + h + 10)
            x1 = max(0, x - 10)
            x2 = min(frame.shape[1], x + w + 10)
            
            primary_face_crop = frame[y1:y2, x1:x2]

            # 4. Run the database search ONLY on the primary cropped face
            results = DeepFace.find(
                img_path=primary_face_crop, 
                db_path=self.db_path, 
                enforce_detection=False,
                silent=True # Stops DeepFace from printing huge logs every 90 frames
            )

        except Exception as e:
            print("DeepFace Security Audit error:", e)
            return None

        # 5. Evaluate the match
        if len(results) > 0 and not results[0].empty:
            match_path = str(results[0]['identity'][0])
            self.current_user = os.path.basename(os.path.dirname(match_path))
            return match_path
            
        return None