from deepface import DeepFace
import cv2
import mediapipe as mp
import numpy as np
import os

class FaceHandler:
    def __init__(self, path):
        self.db_path = path
        self.current_user = None

    def is_authorized(self,frame):
        try:
            results = DeepFace.find(frame, db_path=self.db_path,enforce_detection=True)
        except Exception as e:
            print("DeepFace.find error:", e)
            return None

        if len(results) > 0 and not results[0].empty:
            match_path = str(results[0]['identity'][0])
            # Keep the display name as the folder containing the matched image
            self.current_user = os.path.basename(os.path.dirname(match_path))
            return match_path
        return None