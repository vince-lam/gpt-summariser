import os
import sys
import warnings

from numba import NumbaDeprecationWarning

warnings.filterwarnings("ignore", category=NumbaDeprecationWarning)
import whisper
from whisper.utils import get_writer


def transcribe(audio_path, format="txt", output_path="outputs/transcripts"):
    """
    Transcribe the audio file using Whisper model at the given path and save the transcript to a file.

    Args:
        audio_path (str): The path to the audio file to transcribe.

    Returns:
        str: The path to the file containing the transcript.
    """
    # Load the Whisper model
    model = whisper.load_model("tiny.en")

    # Transcribe the audio
    transcript = model.transcribe(audio_path)

    # Save the transcript to a file
    audio_filename = os.path.basename(audio_path)

    if format == "vtt":
        vtt_writer = get_writer("vtt", output_path)
        vtt_writer(transcript, audio_filename)
    else:
        txt_writer = get_writer("txt", output_path)
        txt_writer(transcript, audio_filename)

    filename = os.path.splitext(os.path.basename(audio_path))[0] + "." + format
    text_path = os.path.join(output_path, filename)

    return text_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        audio_path = sys.argv[1]
        format = sys.argv[2]
        text_path = transcribe(audio_path, format=format)
        print(f"Transcript saved to:\n{text_path}")
    else:
        print("Usage:\npython3 -m gpt_summariser.transcribe_audio <audio_path>")
