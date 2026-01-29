# Towards Intelligent Classrooms: Real-Time Student Attention Analysis and Lecture Summarization

## 📚 Overview

This project implements an intelligent classroom monitoring system that combines computer vision and machine learning to track student attention in real-time. The system uses facial recognition for authentication and gaze/head pose estimation to analyze student engagement during lectures.

## ✨ Features

### 🔐 Facial Recognition Authentication
- Secure student identification using DeepFace
- Face database management for authorized users
- Real-time face detection and matching

### 👁️ Attention Tracking
- Real-time gaze direction analysis using MediaPipe Face Landmarker
- Head pose estimation (pitch and yaw angles)
- Attention state classification:
  - **Focused**: Student is looking directly at the screen/lecture
  - **Distracted**: Student is looking away (up, down, left, or right)
  - **Missing**: No face detected in frame

### 📊 Session Analytics
- Frame-by-frame attention tracking
- Comprehensive session summaries with percentage breakdowns
- Attention statistics (Focused, Distracted, Missing time)

## 🛠️ Technology Stack

- **Computer Vision**: OpenCV, MediaPipe
- **Face Recognition**: DeepFace
- **Deep Learning**: TensorFlow, Keras
- **Image Processing**: NumPy, Pillow
- **User Input**: pynput

## 📋 Requirements

```
opencv-python==4.8.1.78
mediapipe==0.10.8
numpy==1.24.3
deepface==0.0.79
tensorflow==2.15.0
keras==2.15.0
Pillow==10.1.0
gdown==4.7.1
tqdm==4.66.1
pandas==2.0.3
pynput==1.8.1
protobuf==3.20.1
```

## 🚀 Installation

1. **Clone the repository**
```bash
git clone https://github.com/Zzzoorroo/Towards-Intelligent-Classrooms-Real-Time-Student-Attention-Analysis-and-Lecture-Summarization.git
cd Towards-Intelligent-Classrooms-Real-Time-Student-Attention-Analysis-and-Lecture-Summarization
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Download the Face Landmarker model**
   - Download `face_landmarker.task` from [MediaPipe Models](https://developers.google.com/mediapipe/solutions/vision/face_landmarker#models)
   - Place it in the root directory of the project

4. **Set up face database**
   - Create a `data/face_db` directory structure
   - Organize student photos in subdirectories by name:
   ```
   data/face_db/
   ├── StudentName1/
   │   ├── photo1.jpg
   │   └── photo2.jpg
   └── StudentName2/
       ├── photo1.jpg
       └── photo2.jpg
   ```

## 💻 Usage

1. **Run the main client**
```bash
python main_client.py
```

2. **Authentication Phase**
   - The system will access your webcam
   - Position your face in front of the camera
   - Wait for facial recognition to authenticate you

3. **Attention Tracking Phase**
   - Once authenticated, attention tracking begins automatically
   - The system tracks your gaze and head pose
   - Metrics are calculated every 30 frames
   - Press 'q' to quit and view session summary

4. **View Results**
   - After ending the session, you'll see:
     - Total frames processed
     - Percentage of time spent focused
     - Percentage of time spent distracted
     - Percentage of time missing from frame

## 📁 Project Structure

```
.
├── main_client.py              # Main application entry point
├── requirements.txt            # Python dependencies
├── face_landmarker.task       # MediaPipe face landmark model
├── data/
│   └── face_db/               # Face database for authentication
└── src/
    └── modules/
        ├── face_module.py     # Facial recognition handler
        ├── attention.py       # Attention tracking logic
        └── nlp_module.py      # NLP module (for future features)
```

## 🔧 How It Works

### 1. Authentication Flow
- Captures video frames from webcam
- Uses DeepFace to match detected face against database
- Grants access if a match is found

### 2. Attention Tracking
- Uses MediaPipe Face Landmarker to detect 468 facial landmarks
- Calculates head pose using specific landmark points (33, 263, 1, 61, 291, 199)
- Employs PnP (Perspective-n-Point) algorithm to estimate 3D head orientation
- Classifies attention based on pitch and yaw angles:
  - Pitch < -10°: Looking Down
  - Pitch > 10°: Looking Up
  - Yaw < -10°: Looking Right
  - Yaw > 10°: Looking Left
  - Otherwise: Focused

### 3. Statistics Collection
- Samples attention state every 30 frames
- Aggregates data throughout the session
- Calculates percentage distribution of attention states

## 🎯 Use Cases

- **Educational Institutions**: Monitor student engagement in online/hybrid classes
- **Corporate Training**: Track trainee attention during virtual sessions
- **Personal Study**: Self-assessment of focus during independent study
- **Research**: Analyze attention patterns and learning effectiveness

## 🔮 Future Enhancements

The project structure includes an `nlp_module.py` for future integration of:
- Lecture transcription and summarization
- Automatic note generation
- Question-answer systems based on lecture content
- Correlation between attention metrics and content difficulty

## ⚠️ Privacy & Ethics

This system is designed for educational purposes. When deploying:
- Obtain proper consent from all participants
- Comply with local privacy and data protection regulations
- Store and handle biometric data securely
- Be transparent about data collection and usage

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## 📄 License

This project is available for educational and research purposes.

## 👨‍💻 Author

Developed as part of research towards intelligent classroom systems.

---

**Note**: Ensure you have a working webcam and proper lighting for optimal face detection and attention tracking performance.