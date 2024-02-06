import os


def slugify(filename):
    """
    Converts a filename into a slug format by replacing spaces, dots, and dashes with underscores,
    and converting the filename to lowercase.

    Args:
        filename (str): The filename to be slugified.

    Returns:
        str: The slugified filename.
    """
    return filename.replace(" ", "_").replace(".", "_").replace("-", "_").lower()


def get_filename_without_file_extension(path):
    """
    Returns the filename without the file extension.

    Args:
        path (str): The path to the file.

    Returns:
        str: The filename without the file extension.
    """
    return os.path.splitext(os.path.basename(path))[0]
