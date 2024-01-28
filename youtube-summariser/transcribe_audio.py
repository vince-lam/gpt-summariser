import os
import sys

import whisper

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        text_path = transcribe(audio_path)
        print(f"Transcript saved to {text_path}")
    else:
        print("Usage python3 -m youtube-summariser.transcribe_audio.py <audio_path>")
