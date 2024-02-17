import os
import sys
import timeit

import ollama
import spacy
import tiktoken

from .utils import get_filename_without_file_extension


PROMPT = """
<|im_start|>
As a world class transcript summarizer, create a bullet point summary of the
transcript provided.

First include a suitable title for the summary based on the title within the <TITLE> delimiter.
Then include the bullet point summary of the text within the <TEXT> delimiter.

The format of your response needs to be in markdown formatting. Use "- " for bullet points.

Do not just list the general topic or makes things up, only list the actual facts shared.

For example, if a speaker claims that "an increase in X leads to a decrease in
Y", then you should include that claim in the summary, rather than saying "the
speaker discussed the relationship between X and Y".

After you have made all bullet points, add one more bullet point that summarizes
the main point of the text. Here is an example:

- Main message: <MAIN MESSAGE HERE>

######

<TITLE>
{title}

<TEXT>
{chunk}
<|im_end|>
"""

OLLAMA_MODEL = "mistral-openorca"
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

        if sum([count_tokens(chunk) for chunk in current_chunk]) + sent_tokens > max_tokens:
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


def summarise(chunk=None, title=None):
    prompt = PROMPT.format(chunk=chunk, title=title)
    print("Prompt sent to Ollama.")
    result = ollama.chat(
        model=OLLAMA_MODEL,
        messages=[{"role": "user", "content": prompt}],
        stream=False,
    )
    return result


def summarise_all(chunks, title=None):
    summaries = []
    for chunk in chunks:
        result = summarise(chunk, title=title)
        summaries.append(result)
    return summaries


def save_summaries(summaries, filename, output_dir="outputs/summaries"):
    summary_path = os.path.join(output_dir, f"{filename}.txt")
    with open(summary_path, "w") as f:
        for summary in summaries:
            f.write(summary["message"]["content"])
            f.write("\n")

    return summary_path


def summarise_transcript(text_path=None, title=None):
    start_time = timeit.default_timer()
    chunks, total_token_count = split_text(text_path, title=title)
    filename = get_filename_without_file_extension(text_path)
    summaries = summarise_all(chunks, title=title)
    summary_path = save_summaries(
        summaries=summaries,
        filename=filename,
    )
    end_time = timeit.default_timer()
    elapsed_time = int(end_time - start_time)
    print(f"Total input token count: {total_token_count}")
    print(f"Time taken: {elapsed_time} seconds")
    print(f"Summary saved to:\n{summary_path}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        text_path = sys.argv[1]
        title = sys.argv[2]
        summarise_transcript(text_path, title)

    else:
        print("Usage: python3 -m gpt_summariser.summarise_transcript <transcript_path> <title>")
