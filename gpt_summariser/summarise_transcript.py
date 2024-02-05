import os
import sys
import timeit

import openai
import spacy
import tiktoken
from dotenv import load_dotenv
from openai import OpenAI

from .utils import get_filename_without_file_extension

load_dotenv()

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


def split_text(text_path=None, title=None):
    prompt_tokens = count_tokens(PROMPT.format(chunk="", title=title))
    max_tokens = MODEL_MAX_TOKENS - prompt_tokens - RESPONSE_TOKENS

    nlp = spacy.load("en_core_web_sm")
    nlp.add_pipe("sentencizer")

    with open(text_path, "r") as f:
        text = f.read()

    doc = nlp(text, disable=["tagger", "parser", "ner", "lemmatizer", "textcat"])
    chunks = []
    current_chunk = []

    for sent in doc.sents:
        sent_text = sent.text.strip()  # This is one sentence
        sent_tokens = count_tokens(sent_text)

        if (
            sum([count_tokens(chunk) for chunk in current_chunk]) + sent_tokens
            > max_tokens
        ):
            # If adding sentence to the current chunk will exceed the token
            # limit, add the current chunk to the list of chunks and start a new
            # chunk with the current sentence
            chunks.append(" ".join(current_chunk))
            current_chunk = [sent_text]
        else:
            # If adding sentence to the current chunk will not exceed the token
            # limit, add the sentence to the current chunk
            current_chunk.append(sent_text)

    if current_chunk:
        chunks.append(" ".join(current_chunk))

    total_token_count = sum([count_tokens(chunk) for chunk in chunks])
    return chunks, total_token_count


def summarise(chunks, filename, title):
    client = openai.Client(api_key=os.getenv("OPENAI_API_KEY"))

    summaries = []
    for chunk in chunks:
        prompt = PROMPT.format(chunk=chunk, title=title)
        prompt_tokens = count_tokens(prompt)
        result = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=RESPONSE_TOKENS,
            temperature=0,
            n=1,
            stream=False,
        )
        summaries.append(result)

    summmary_path = os.path.join("outputs/summaries", f"{filename}_summary.txt")
    with open(summmary_path, "w") as f:
        for summary in summaries:
            f.write(summary.choices[0].message.content)
            f.write("\n")

    return summmary_path


if __name__ == "__main__":
    if len(sys.argv) > 1:
        start_time = timeit.default_timer()
        text_path = sys.argv[1]
        chunks, total_token_count = split_text(text_path)
        filename = get_filename_without_file_extension(text_path)
        summary_path = summarise(chunks, filename)
        end_time = timeit.default_timer()
        elapsed_time = int(end_time - start_time)
        print(f"Summary saved to:/n{summary_path}")
        print(f"Total token count: {total_token_count}")
        print(f"Time taken: {elapsed_time} seconds")
    else:
        print("Usage: python3 -m gpt_summariser.summarise_transcript <transcript_path>")
