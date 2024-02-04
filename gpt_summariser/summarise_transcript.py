import os
import sys
import openai
import spacy
import tiktoken

from dotenv import load_dotenv
from .utils import get_filename_without_file_extension

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

PROMPT = """You are an expert at text summarisation and have been asked to 
create a bullet point summary of the transcript that follows the delimiter 
### TEXT ###. 

Do not just list the general topic, but list the actual facts shared.

For example, if a speaker claims that "an increase in X leads to a decrease in 
Y", then you should include that claim in the summary, rather than saying "the 
speaker discussed the relationship between X and Y".

Use "- " for bullet points.

After you have made all bullet points, add one more bullet point that summarises
the main point of the text. Here is an example:

- Main message: <MAIN MESSAGE HERE>

#######

TEXT TITLE: {title}

### TEXT ###
{chunk}
"""

MODEL = "gpt-3.5-turbo-0125"
ENCODING = "cl100k_base"
MODEL_MAX_TOKENS = 16384
COST_PER_1L_INPUT_TOKENS_USD = 0.0005
COST_PER_1K_OUTPUT_TOKENS_USD = 0.0015
REPONSE_TOKENS = 4000


def count_tokens(text):
    """Count tokens in a text string with tiktoken"""
    enc = tiktoken.encoding_for_model(MODEL)
    tokens = enc.encode(text)
    token_count = len(tokens)
    return token_count


def get_sentences(text_path):
    with open(text_path, "r") as f:
        text = f.read()

    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    sentences = [sent.text.strip() for sent in doc.sents]

    return sentences


def get_chunks(sentences):
    return ["This is a chunk"]


def summarise(chunks, filename):
    return "outputs/summaries/summary.txt"


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
