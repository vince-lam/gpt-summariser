import os
import sys
from datetime import datetime
from .utils import slugify, get_filename_without_file_extension

import yt_dlp


def download_audio(youtube_url, output_path="outputs/audio"):
    # List to store downloaded filenames
    downloaded_filenames = []

    def my_hook(info_dict):
        if info_dict["status"] == "finished":
            return None

        filename = info_dict["filename"]
        # Replace the original extension with .wav
        wav_filename = os.path.splitext(filename)[0] + ".wav"
        print(f"\n\nDownload complete, now converting:\n{filename}")
        downloaded_filenames.append(wav_filename)

    # Ensure the output directory exists
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # Options for downloading audio in best format and converting to wav
    ydl_opts = {
        "format": "bestaudio/best",
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "progress_hooks": [my_hook],
    }

    # Downloading the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Assuming only one file is downloaded, return the first item in the list
    # Rename the file with today's date
    if downloaded_filenames:
        final_path = downloaded_filenames[0]
        return final_path
    else:
        return None


# Example usage
# url = "≈" # 5 second video
"""url = "https://www.youtube.com/watch?v=0NcPkQsKZSQ"  # 10 minute video
output_file = download_audio(url)
print(f"Downloaded audio file path: {output_file}")"""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
        audio_path = download_audio(youtube_url)
        print(f"\nDownloaded audio file path:\n{audio_path}\n")
    else:
        print("Usage:\npython -m gpt_summariser.download_yt_audio <youtube_url>")
