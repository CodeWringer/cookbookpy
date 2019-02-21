from classes.asset_content import AssetContent
from utility.url import get_url
import markdown
import os

class AssetMarkdown(AssetContent):
    """Represents a markdown document."""
    def __init__(self, file_path):
        super().__init__(file_path)
        self.markdown = self.get_markdown()

    def get_markdown(self):
        """Analyzes the file found via the given absolute path."""
        return super().get_section(_('Markdown'))

    def render(self, generator, dest_dir):
        """Renders and writes out this asset."""
        # Render self.
        super().render(generator, dest_dir)

    def get_rendered(self, generator):
        """Returns an html representation of this asset."""
        categories_toc = self.parent.get_rendered_for_toc()
        title = self.title
        titleimage = None # TODO

        categories = []
        for category in generator.root_category.children:
            categories.append({ 'name': category.name,
                                'url': get_url(self.path,
                                               category.file_path) })

        neighbor_previous = None
        neighbor_next = None
        if len(self.navigation.neighbors_prev) > 0:
            neighbor = self.navigation.neighbors_prev[0]
            neighbor_previous = {
                'title': neighbor.title,
                'url': get_url(self.path,
                               neighbor.path)
            }
        if len(self.navigation.neighbors_next) > 0:
            neighbor = self.navigation.neighbors_next[0]
            neighbor_next = {
                'title': neighbor.title,
                'url': get_url(self.path,
                               neighbor.path)
            }

        content = markdown.markdown('\n'.join(self.markdown), ['extra'])
        # see_also = TODO

        rendered = generator.templates['template_base'].render(
            language = generator.language,
            styles = generator.get_style_urls(self),
            categories_toc = categories_toc,
            categories = categories,
            category = { 'name': self.parent.name },
            title = title,
            titleimage = titleimage,
            neighbor_previous = neighbor_previous,
            neighbor_next = neighbor_next,
            content_override = content,
            # see_also = see_also
        )
        return rendered
