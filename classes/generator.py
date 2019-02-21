import jinja2
from jinja2 import FileSystemLoader
import os
import utility.io
from distutils.dir_util import copy_tree
from classes.category import Category
from classes.navigation import Navigation
from classes.asset import Asset
from utility.url import get_url

class Generator():
    """Core class that generates the cook book."""
    def __init__(self,
                 source_content_dir,
                 destination_content_dir,
                 template_dir,
                 language
                 ):
        if not source_content_dir:
            raise ValueError('source_content_dir must not be None!')
        if not destination_content_dir:
            raise ValueError('destination_content_dir must not be None!')
        if not template_dir:
            raise ValueError('template_dir must not be None!')

        self.source_content_dir = source_content_dir
        self.destination_content_dir = destination_content_dir
        self.theme_dir = os.path.join(source_content_dir, 'theme')
        self.template_dir = template_dir
        self.language = language

        print('--------- [Generator] Getting templates')
        self.templates = self.get_templates()
        print('[Generator] Acquired %s templates' % (str(len(self.templates))))

        print('--------- [Generator] Getting css styles')
        self.styles = self.get_styles()
        print('[Generator] Acquired %s css styles' % (str(len(self.styles))))

        print('--------- [Generator] Getting categories')
        self.root_category = Category(self.source_content_dir)

        print('--------- [Generator] Getting navigation')
        Navigation(self.root_category)

        print('--------- [Generator] Rendering')
        self.render()

    def get_templates(self):
        """Loads and returns the template files."""
        env = jinja2.Environment(
            loader=FileSystemLoader(self.template_dir,
                                    encoding='windows-1252'),
            # autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        path_base = 'template_base.html'
        path_category = 'template_category.html'
        path_recipe = 'template_recipe.html'
        path_toc = 'template_toc.html'

        templates = {}
        templates['template_base'] = env.get_template(path_base)
        templates['template_category'] = env.get_template(path_category)
        templates['template_recipe'] = env.get_template(path_recipe)
        templates['template_toc'] = env.get_template(path_toc)
        return templates

    def get_styles(self):
        """Returns a list of css style file paths."""
        styles = []
        styles_dir = os.path.join(self.source_content_dir, 'theme', 'css')

        style_files = utility.io.get_file_names(styles_dir)
        for style_file in style_files:
            file_path = os.path.join(styles_dir, style_file)
            style_asset = Asset(file_path)
            styles.append(style_asset)
        return styles

    def get_style_urls(self, obj):
        """Returns a list of styles urls for use in template rendering.
        Parameters
        ---------
        obj : Asset or Category
          The object for which to get the urls.
        """
        path = obj.path

        if isinstance(obj, Category):
            path += '/index.html'

        style_urls = []
        for style in self.styles:
            url = get_url(path, style.path)
            style_urls.append({ 'url': url })
        return style_urls

    def render(self):
        """Renders the templates."""
        categories_toc = self.root_category.get_rendered_for_toc()
        style_urls = self.get_style_urls(self.root_category)
        title = _('Table of Contents')
        titleimage = None   # TODO
        rendered_toc = self.templates['template_toc'].render(
                                        language = self.language,
                                        styles = style_urls,
                                        title = title,
                                        titleimage = titleimage,
                                        categories_toc = categories_toc)
        utility.io.ensure_dir(self.destination_content_dir)
        rendered_path = os.path.join(self.destination_content_dir,
                                     'index.html')
        with open(rendered_path, mode='wb') as outfile:
            outfile.write(rendered_toc.encode('utf-8'))

        # Copy theme dir.
        copy_tree(os.path.join(self.source_content_dir, 'theme'),
                  os.path.join(self.destination_content_dir, 'theme'))

        # Render categories, including their children and assets.
        for category in self.root_category.children:
            category.render(self, self.destination_content_dir)

