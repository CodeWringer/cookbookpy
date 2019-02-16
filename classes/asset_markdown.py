from classes.asset import Asset

class AssetMarkdown(Asset):
    """Represents a markdown document."""
    def __init__(self, file_path):
        super().__init__(file_path)
        self.markdown = self.get_markdown()

    def get_markdown(self):
        """Analyzes the file found via the given absolute path."""
        self.markdown = super().get_section(_('Markdown'))
