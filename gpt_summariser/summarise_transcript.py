import os
import sys
import openai
import spacy
import tiktoken

from .utils import get_filename_without_file_extension


def get_sentences():
    pass


def get_chunks():
    pass


def summarise():
    pass


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text_path = sys.argv[1]
        sentences = get_sentences(text_path)
        chunks = get_chunks(sentences)
        filename = get_filename_without_file_extension(text_path)
        summary_path = summarise(chunks, filename)

        print(f"Summary saved to {summary_path}")
    else:
        print("Usage: python3 -m gpt_summariser.summarise_transcript <transcript_path>")
