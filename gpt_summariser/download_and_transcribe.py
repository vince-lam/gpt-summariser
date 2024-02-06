import sys

from .download_yt_audio import download_audio
from .transcribe_audio import transcribe

if __name__ == "__main__":
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
        audio_path = download_audio(youtube_url)
        print(f"\nDownloaded audio file path:\n{audio_path}\n")
        elapsed_time_secs, text_path = transcribe(audio_path)
        print(
            f"Audio transcribed in {elapsed_time_secs} seconds.\nTranscript saved to:\n{text_path}"
        )
    else:
        print("Usage:\npython -m gpt_summariser.download_and_transcribe <youtube_url>")
