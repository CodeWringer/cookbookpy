import os
from os import walk

def get_directory_names(directory):
    """Returns the names of all the sub directories in the given directory."""
    return [name for name in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, name))]

def get_file_names(directory):
    """Returns the names of all the files in the given directory."""
    f = []
    for (dirpath, dirnames, filenames) in walk(directory):
        f.extend(filenames)
        break
    return f

def ensure_dir(directory):
    """Creates the full directory path to the given directory, if it doesn't exist."""
    print('Ensuring directory ' + directory)
    if not os.path.exists(directory):
        os.makedirs(directory)

def get_file_text(path, encoding):
    """Returns all text contents of a file at the given path in the form of a string."""
    with open(path, mode='r', encoding=encoding) as f:
        return f.read()

def get_file_text_lines(path, encoding):
    """Returns all text c ontents of a file at the given path in the form of an array."""
    lines = []
    with open(path, mode='r', encoding=encoding) as f:
        lines = f.readlines()
    return lines

def get_file_exists(path):
    """Returns true, if a file exists at the given path."""
    return os.path.exists(path)

def get_new_ext(path, ext):
    """Returns the given file path, with the file extension changed to the given extension."""
    if not ext.startswith('.'):
        ext = '.' + ext
    # os.path.splitext did not behave as expected here -> splitting extension off manually.
    index = path.rfind('.')
    asset_path = path[:index]
    asset_path = asset_path + ext
    return asset_path
