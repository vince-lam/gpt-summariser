import os
import sys

import yt_dlp


def download_audio(youtube_url: str, output_path: str = "outputs/audio"):
    """
    Downloads audio from a YouTube video and saves it as a WAV file.

    Args:
        youtube_url (str): The URL of the YouTube video.
        output_path (str, optional): The path to save the downloaded audio file. Defaults to "outputs/audio".

    Returns:
        str: The path of the downloaded audio file.
    """
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
    }

    # Downloading the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(youtube_url, download=True)
        filename = ydl.prepare_filename(info_dict)
        # Change the extension to wav, as it's the format we're saving in
        wav_filename = os.path.splitext(filename)[0] + ".wav"
        return wav_filename


if __name__ == "__main__":
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
        audio_path = download_audio(youtube_url)
        print(f"Downloaded audio file path: {audio_path}")
    else:
        print("Usage: python -m youtube-summariser.download_yt_audio.py <youtube_url>")

""" TEST
url = "https://youtube.com/watch?v=1O0yazhqaxs"
output_file = download_audio(url)
print(f"Downloaded audio file path: {output_file}")
"""
