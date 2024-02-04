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
COST_PER_1K_INPUT_TOKENS_USD = 0.0005
COST_PER_1K_OUTPUT_TOKENS_USD = 0.0015
RESPONSE_TOKENS = 4000


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
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        # Check if adding the next sentence to the current chunk will exceed the
        # token limit
        new_chunk = f"{current_chunk} {sentence}"
        new_chunk_token_count = (
            count_tokens(PROMPT.format(chunk=new_chunk)) + RESPONSE_TOKENS
        )

        if new_chunk_token_count <= MODEL_MAX_TOKENS:
            # If not, add sentence to current chunk
            current_chunk = new_chunk.strip()
        else:
            # If yes, start a new chunk with the current sentence
            chunks.append(current_chunk)
            current_chunk = sentence.strip()

    # Add the last chunk if it is not empty
    if current_chunk:
        chunks.append(current_chunk)

    return chunks


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
