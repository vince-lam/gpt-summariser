import os
import sys

from newspaper import Article


def download_website_text(url, title, output_path="outputs/website"):
    article = Article(url)
    article.download()
    article.parse()

    # Access article attributes
    print(article.authors)
    print(article.publish_date)
    print(article.text)
    filename = f"{title}.txt"
    file_path = os.path.join(output_path, filename)
    with open(file_path, "w") as f:
        f.write(f"Author: {article.authors}\n")
        f.write(f"Publish date: {article.publish_date}\n\n")
        f.write(article.text)
    return file_path, article.text


if __name__ == "__main__":
    if len(sys.argv) > 1:
        url = sys.argv[1]
        title = sys.argv[2]
        file_path, text = download_website_text(url, title)
        print(f"\nDownloaded audio file path:\n{file_path}\n")
    else:
        print("Usage:\npython -m gpt_summariser.download_text <url> <title>")
