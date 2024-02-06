import os
import sys
from datetime import datetime

import yt_dlp

from .utils import get_filename_without_file_extension, slugify


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

    date_str = datetime.now().strftime("%Y-%m-%d_")
    outtmpl = os.path.join(output_path, date_str + "%(title)s.%(ext)s")

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
        "outtmpl": outtmpl,
        "progress_hooks": [my_hook],
    }

    # Downloading the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Assuming only one file is downloaded, return the first item in the list
    if downloaded_filenames:
        output_file_path = downloaded_filenames[0]
        original_path, original_filename = os.path.split(output_file_path)
        original_file_base, file_ext = os.path.splitext(original_filename)
        slugified_base = slugify(original_file_base)
        new_file_path = os.path.join(output_path, f"{slugified_base}{file_ext}")
        os.rename(output_file_path, new_file_path)
        return new_file_path
    else:
        return None


if __name__ == "__main__":
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
        audio_path = download_audio(youtube_url)
        print(f"\nDownloaded audio file path:\n{audio_path}\n")
    else:
        print("Usage:\npython -m gpt_summariser.download_yt_audio <youtube_url>")
