# Path: src/core/audio_handler.py

import pyaudio
import wave

class AudioHandler:
    """Handles audio input and output."""

    def __init__(self, sample_rate=16000, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.audio_stream = None
        self.frames = []

    def start_recording(self):
        """Starts recording audio."""
        self.audio_stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                                  channels=self.channels,
                                                  rate=self.sample_rate,
                                                  input=True,
                                                  frames_per_buffer=1024)
        print("Recording started...")

    def stop_recording(self):
        """Stops recording audio."""
        if self.audio_stream:
            self.audio_stream.stop_stream()
            self.audio_stream.close()
            print("Recording stopped.")
            self.audio_stream = None

    def save_audio(self, filename):
        """Saves the recorded audio to a WAV file."""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(pyaudio.PyAudio().get_sample_size(pyaudio.paInt16))
            wf.setframerate(self.sample_rate)
            wf.writeframes(b''.join(self.frames))
        print(f"Audio saved to {filename}")
        self.frames = []