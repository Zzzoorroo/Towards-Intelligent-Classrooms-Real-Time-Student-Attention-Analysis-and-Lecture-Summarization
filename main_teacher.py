import threading
from src.modules.recorder import AudioRecorder
from src.modules.transcriber import AudioTranscriber

print("Initializing Continuous Teacher System...")

# 1. Instantiate modules
mic = AudioRecorder()
ai_scribe = AudioTranscriber(model_size="base")
master_transcript_file = "full_lecture_transcript.txt"

# Clear the old transcript if it exists
with open(master_transcript_file, "w") as f:
    f.write("--- LECTURE START ---\n")

def process_audio_background(audio_path):
    """This function runs in the background. It transcribes and saves text."""
    print(f"\n🧠 AI Processing: {audio_path}")
    text = ai_scribe.transcribe(audio_path, language="en")
    
    print(f"\n✅ Transcribed: {text}")
    
    # Append the text to the master file
    with open(master_transcript_file, "a", encoding="utf-8") as f:
        f.write(text + " ")

# 2. The Infinite Classroom Loop
print("\n🏫 Classroom Session Started. Press Ctrl+C to end the lecture.")
try:
    while True:
        # A. Record exactly 15 seconds of audio (short duration for testing)
        saved_chunk_path = mic.record_chunk(duration_seconds=15)
        
        # B. Spawn a background thread to process that chunk
        # This allows the loop to instantly restart and record the next chunk!
        processing_thread = threading.Thread(
            target=process_audio_background, 
            args=(saved_chunk_path,)
        )
        processing_thread.start()

except KeyboardInterrupt:
    print("\n🛑 Lecture Ended. Waiting for final AI processing to finish...")
    # The script will naturally wait for the last transcription thread to complete