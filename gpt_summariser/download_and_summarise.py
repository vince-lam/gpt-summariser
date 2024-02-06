import sys

from .download_yt_audio import download_audio
from .transcribe_audio import transcribe
from .summarise_transcript import summarise_transcript

if __name__ == "__main__":
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
        title = sys.argv[2]
        audio_path = download_audio(youtube_url)
        print(f"\nDownloaded audio file path:\n{audio_path}\n")
        elapsed_time_secs, text_path = transcribe(audio_path)
        print(
            f"Audio transcribed in {elapsed_time_secs} seconds.\nTranscript saved to:\n{text_path}"
        )
        summarise_transcript(text_path, title)
    else:
        print(
            "Usage: python3 -m gpt_summariser.download_and_summarise <transcript_path> <title>"
        )
