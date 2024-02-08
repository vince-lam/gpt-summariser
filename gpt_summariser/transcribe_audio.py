import argparse
import json
import os
import re
import sys
import timeit

from dotenv import load_dotenv

from .utils import get_filename_without_file_extension

load_dotenv()

# if statement is env environment is available use env variable else use default
if os.getenv("REPO_PATH") is None:
    repo_path = os.getcwd()
else:
    repo_path = os.getenv("REPO_PATH")


def transcribe_to_json(audio_path, output_path="outputs/transcripts"):
    filename_no_ext = get_filename_without_file_extension(audio_path)
    json_file_path = os.path.join(repo_path, output_path, filename_no_ext + ".json")

    start_time = timeit.default_timer()
    cmd = (
        f"insanely-fast-whisper"
        f' --file-name "{audio_path}"'
        f" --device-id mps"
        f" --model-name distil-whisper/distil-small.en"
        f" --batch-size 4"
        f" --transcript-path {json_file_path}"
    )
    os.system(cmd)

    end_time = timeit.default_timer()
    elapsed_time = int(end_time - start_time)

    return elapsed_time, json_file_path


def get_text_from_json(json_path):
    with open(json_path, "r") as json_file:
        json_data = json.load(json_file)
        text = json_data["text"]
    return text


def save_text_to_txt(json_path, output_path):
    text = get_text_from_json(json_path)
    text = re.sub(r"(?<=[.!?])\s+", "\n", text)
    with open(output_path, "w") as txt_file:
        txt_file.write(text)


def change_file_path_extension(file_path, new_extension):
    return os.path.splitext(file_path)[0] + "." + new_extension


def remove_json_file(json_path):
    os.remove(json_path)


def transcribe(audio_path, output_path="outputs/transcripts"):
    elapsed_time, json_file_path = transcribe_to_json(audio_path, output_path)
    txt_file_path = change_file_path_extension(json_file_path, "txt")

    save_text_to_txt(json_path=json_file_path, output_path=txt_file_path)
    remove_json_file(json_path=json_file_path)
    return elapsed_time, txt_file_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        parser = argparse.ArgumentParser(description="Transcribe audio file.")
        parser.add_argument(
            "audio_path", type=str, help="The path to the audio file to transcribe."
        )
        parser.add_argument(
            "--output_path",
            type=str,
            default="outputs/transcripts",
            help="The path to save the transcript.",
        )
        args = parser.parse_args()

        elapsed_time, txt_file_path = transcribe(
            args.audio_path, output_path=args.output_path
        )
        print(
            f"Audio transcribed in {elapsed_time} seconds.\nTranscript saved to:\n{txt_file_path}"
        )
    else:
        print("Usage:\npython3 -m gpt_summariser.transcribe_audio <audio_path>")
