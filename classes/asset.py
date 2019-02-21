import utility.io
import os

class Asset():
    """Model class that represents an asset file."""
    def __init__(self, path):
        self.path = path
        self.name = os.path.basename(path)
        self.text_content = self.get_content()

    def get_content(self):
        """Loads the file contents as text from disk an returns an array of text lines."""
        return utility.io.get_file_text_lines(self.path, encoding='windows-1252')

    def render(self, generator, dest_dir_path):
        pass
