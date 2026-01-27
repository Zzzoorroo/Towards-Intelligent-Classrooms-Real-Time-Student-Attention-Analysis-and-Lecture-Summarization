import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import numpy as np

import os

class AttentionTracker:
    def __init__(self, model_filename='face_landmarker.task'):
        # Get the absolute path to the directory where this script is located
        # If this script is in src/modules/, we might need to go up levels depending on where the .task file is.
        # Assuming you put the .task file in the ROOT folder (where main_client.py is):
        
        cwd = os.getcwd() # Gets the current working directory
        model_path = os.path.join(cwd, model_filename)

        print(f"Loading model from: {model_path}") # Debug print to check path

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}. Please download it.")

        base_options = python.BaseOptions(model_asset_path=model_path)
        options = vision.FaceLandmarkerOptions(
            base_options=base_options,
            output_face_blendshapes=True,
            num_faces=1
        )
        self.detector = vision.FaceLandmarker.create_from_options(options)
    def get_attention_metrics(self, frame):
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # 3. MediaPipe Tasks requires a 'MediaPipe Image' object
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        
        # 4. Perform detection
        detection_result = self.detector.detect(mp_image)
        
        img_h, img_w, _ = rgb_frame.shape

        if not detection_result.face_landmarks:
            return {"status": "No Face Detected", "score": 0}

        face_3d = []
        face_2d = []

        # 5. Extract landmarks (Tasks API uses a list of lists)
        for face_landmarks in detection_result.face_landmarks:
            for idx in [33, 263, 1, 61, 291, 199]:
                lm = face_landmarks[idx]
                x, y = int(lm.x * img_w), int(lm.y * img_h)
                face_2d.append([x, y])
                face_3d.append([x, y, lm.z])

            face_2d = np.array(face_2d, dtype=np.float64)
            face_3d = np.array(face_3d, dtype=np.float64)

            # --- Remaining PnP Logic is the same ---
            focal_length = 1 * img_w
            cam_matrix = np.array([[focal_length, 0, img_w/2],
                                   [0, focal_length, img_h/2],
                                   [0, 0, 1]])
            dist_matrix = np.zeros((4, 1), dtype=np.float64)
            
            _, rot_vec, _ = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)
            rmat, _ = cv2.Rodrigues(rot_vec)
            angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

            pitch = angles[0] * 360
            yaw = angles[1] * 360

            # Thresholding
            if pitch < -10: status = "Looking Down"
            elif pitch > 10: status = "Looking Up"
            elif yaw < -10: status = "Looking Left"
            elif yaw > 10: status = "Looking Right"
            else: status = "Focused"

            return {
                "status": status,
                "pitch": round(pitch, 2),
                "yaw": round(yaw, 2)
            }