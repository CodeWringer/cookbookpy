from classes.asset_content import AssetContent
import markdown

class AssetMarkdown(AssetContent):
    """Represents a markdown document."""
    def __init__(self, file_path):
        super().__init__(file_path)
        self.markdown = self.get_markdown()

    def get_markdown(self):
        """Analyzes the file found via the given absolute path."""
        return super().get_section('Markdown')

    def render(self, generator, dest_dir):
        """Renders and writes out this asset."""
        # Render self.
        super().render(generator, dest_dir)

    def get_rendered(self, generator):
        """Returns an html representation of this asset."""
        categories_toc = self.parent.get_rendered_for_toc()
        title = self.title
        titleimage = None # TODO

        categories = self.get_categories(generator)
        neighbor_previous = self.get_neighbor_prev()
        neighbor_next = self.get_neighbor_next()

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
