# GPT Summarisation App

The GPT Summarization App is a powerful tool designed to streamline the process of extracting and summarising content from YouTube videos. By leveraging the capabilities of OpenAI's Whisper model for accurate transcription and the GPT-3.5 API for concise summarisation, this app offers a seamless workflow for users to input a YouTube URL and receive a summarised text of the video's audio content.

## Features

* **YouTube Audio Download:** Automatically downloads the audio track of any YouTube video provided via URL.
* **Audio Transcription:** Utilises the Whisper model for state-of-the-art audio transcription, ensuring high accuracy in converting speech to text.
* **Content Summarisation:** Leverages the GPT-3.5 API to produce clear, concise summaries of the transcribed text, making it easy to capture the essence of the video content.

## Getting Started on MacOS

1. Clone this repo
2. Create a virtual environment with `venv`

    ```shell
    python -m venv .venv && source .venv/bin/activate && python -m pip install --upgrade pip
    ```

3. Install dependencies

    ```shell
    pip install -r requirements.txt
    ```

4. Install homebrew
5. Install `ffmpeg` with `brew install ffmpeg`
6. Download the `spacy` model:

    ```shell
    python -m spacy download en_core_web_sm
    ```

7. Install `insanely-fast-whisper` for transcriptions:

    ```shell
    pipx install insanely-fast-whisper --force --pip-args="--ignore-requires-python"
    ```

8. Create `.env` in root directory and add your OpenAI API key:

    ```env
    OPENAI_API_KEY='add your OpenAI API key here' # https://platform.openai.com/account/api-keys
    ```

## Usage

* Run the app from the command line, passing the YouTube URL as an argument. To download and transcribe a Youtube video, run this command:

    ``` shell
    python -m gpt_summariser.download_and_transcribe <youtube_url>
    ```

* To download and summarise a Youtube video, run this command:

    ``` shell
    python -m gpt_summariser.download_and_summarise <youtube_url> <title>
    ```

## Repo structure

``` shell
.
├── LICENSE
├── README.md
├── gpt_summariser
│   ├── __init__.py
│   ├── download_and_summarise.py
│   ├── download_and_transcribe.py
│   ├── download_yt_audio.py
│   ├── summarise_transcript.py
│   ├── transcribe_audio.py
│   └── utils.py
├── outputs
│   ├── audio
│   ├── summaries
│   └── transcripts
└── requirements.txt
```

## TODO

* [x] Download the YouTube video as a `wav` audio file
* [x] Transcribe audio file using OpenAI's Whisper model to `txt` or `vtt` formats
* [x] Summarise the transcript using free models from HuggingFace
* [x] Transcribe audio file using `insanely-fast-whisper` and `distil-whisper` for faster transcriptions
* [ ] Add documentation
* [ ] Add tests
* [ ] Use free open-source models for summarisation instead of GPT3.5
* [ ] Add speaker diarisation support
* [ ] If the YouTube URL is in the `youtu.be` format, then convert it to the `/watch?v=` format
* [ ] Output transcripts and summaries into logseq `markdown` format
* [ ] Add front-end UI
* [ ] Add support for `pdf` and `epub` formats
* [ ] Batch downloads and summarisations
* [ ] Dockerise app

## Contributing

Contributions are welcome! If you'd like to improve the GPT Summarisation App, please fork the repository and submit a pull request with your proposed changes.

## License

This project is licensed under the MIT License - see the `LICENSE.md` file for details.
