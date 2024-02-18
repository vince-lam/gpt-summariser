import os
import re


def slugify(text):
    # Convert to lowercase
    text = text.lower()
    # Replace spaces with hyphens
    text = text.replace(" ", "-")
    # Remove characters that are not alphanumeric or hyphens
    text = re.sub(r"[^a-z0-9\-]", "", text)
    # Replace multiple hyphens with a single hyphen
    text = re.sub(r"-+", "-", text)
    # Trim hyphens from the start and end of the text
    text = text.strip("-")
    return text


def get_filename_without_file_extension(path):
    """
    Returns the filename without the file extension.

    Args:
        path (str): The path to the file.

    Returns:
        str: The filename without the file extension.
    """
    return os.path.splitext(os.path.basename(path))[0]
