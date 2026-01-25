from deepface import DeepFace
import os 

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'#silence tensor flow logging
DeepFace.stream(db_path='face_db')