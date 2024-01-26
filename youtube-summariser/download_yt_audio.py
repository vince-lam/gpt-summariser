import logging
import os
import sys
from datetime import datetime

import yt_dlp


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def rename_file_with_date(original_path):
    # Catch any OSError exceptions that might occur during the file renaming.
    try:
        directory, filename = os.path.split(original_path)
        name, extension = os.path.splitext(filename)

        # Get today's date in YYYY-MM-DD format
        today = datetime.now().strftime("%Y-%m-%d")

        # Create a new filename with today's date
        new_filename = f"{name}_{today}{extension}"
        new_path = os.path.join(directory, new_filename)

        # Log the renaming attempt
        logging.info(f"Attempting to rename file from {original_path} to {new_path}")

        # Rename the file
        os.rename(original_path, new_path)

        # Log successful renaming
        logging.info(f"Successfully renamed file to {new_path}")

        return new_path
    except OSError as e:
        # Log detailed error information
        logging.error(
            f"Error renaming file from {original_path} to {new_path}: {e.strerror}"
        )
        return None


def download_audio(youtube_url, output_path="outputs/audio"):
    # List to store downloaded filenames
    downloaded_filenames = []

    def my_hook(d):
        if d["status"] == "finished":
            filename = d["filename"]
            # Replace the original extension with .wav
            wav_filename = os.path.splitext(filename)[0] + ".wav"
            print(f"\n\nDownload complete, now converting:\n{d['filename']}")
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
        final_path = rename_file_with_date(downloaded_filenames[0])
        return final_path
    else:
        return None


# Example usage
# url = "https://youtube.com/watch?v=1O0yazhqaxs" # 5 second video
"""url = "https://www.youtube.com/watch?v=0NcPkQsKZSQ"  # 10 minute video
output_file = download_audio(url)
print(f"Downloaded audio file path: {output_file}")"""


if __name__ == "__main__":
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
        audio_path = download_audio(youtube_url)
        print(f"\nDownloaded audio file path:\n{audio_path}\n")
    else:
        print("Usage: python -m youtube-summariser.download_yt_audio.py <youtube_url>")
