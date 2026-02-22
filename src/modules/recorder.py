import pyaudio
import wave
import os
from datetime import datetime

class AudioRecorder:
    def __init__(self):
        """Initializes the audio hardware settings for speech."""
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1
        self.rate = 44100
        self.lecture_audio_folder = "lecture_audio"
        # Ensure the folder exists
        if not os.path.exists(self.lecture_audio_folder):
            os.makedirs(self.lecture_audio_folder)

    def record_lecture(self, output_filename=None):
        """Listens to the mic and saves a .wav file."""
        # Generate timestamp-based filename if not provided
        if output_filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_filename = f"{timestamp}.wav"
        
        # Create full path with lecture_audio folder
        output_path = os.path.join(self.lecture_audio_folder, output_filename)
        
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk)

        print("\n🔴 RECORDING... (Press Ctrl+C to stop)")
        frames = []

        try:
            while True:
                data = stream.read(self.chunk)
                frames.append(data)
        except KeyboardInterrupt:
            print("\n🛑 Recording Stopped.")

        stream.stop_stream()
        stream.close()
        p.terminate()

        print(f"💾 Saving audio to {output_path}...")
        wf = wave.open(output_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return output_path
    def record_chunk(self, duration_seconds=30):
        """Records audio for a fixed amount of time and saves it."""
        import os # Ensure os is imported at the top of your file
        from datetime import datetime
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_filename = f"chunk_{timestamp}.wav"
        output_path = os.path.join(self.lecture_audio_folder, output_filename)
        
        p = pyaudio.PyAudio()
        stream = p.open(format=self.format,
                        channels=self.channels,
                        rate=self.rate,
                        input=True,
                        frames_per_buffer=self.chunk)

        print(f"\n🎤 Recording {duration_seconds}-second chunk...")
        frames = []

        # Calculate exactly how many chunks to read based on the duration
        num_chunks = int((self.rate / self.chunk) * duration_seconds)
        
        for _ in range(num_chunks):
            data = stream.read(self.chunk)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(output_path, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(p.get_sample_size(self.format))
        wf.setframerate(self.rate)
        wf.writeframes(b''.join(frames))
        wf.close()
        
        return output_path