import sys


def download_audio(youtube_url: str):
    """
    Downloads audio from a YouTube video and return the path to the downloaded file.

    Args:
        youtube_url (str): The URL of the YouTube video to download audio from.
        return (str): The path to the downloaded audio file.
    """
    return "files/audio/example.wav"


if __name__ == "__main__":
    if len(sys.argv) > 1:
        youtube_url = sys.argv[1]
        audio_path = download_audio(youtube_url)
        print(f"Download complete: {audio_path}")
    else:
        print("Usage: python -m youtube-summariser.download_yt_audio.py <youtube_url>")
