import jinja2
from jinja2 import FileSystemLoader, select_autoescape
import os
import sys
import utility.io
import lxml
from lxml.html import builder as E
from classes.category import Category
from classes.navigation_for_obj import NavigationForObj
from classes.navigation_for_path import NavigationForPath

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
        NavigationForObj(self.root_category)

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
            file_path = os.path.join('theme', 'css', style_file)
            styles.append(file_path)
        return styles

    def get_styles_for_render(self, obj):
        styles = []
        for style in self.styles:
            nav = NavigationForPath(obj, style, self.source_content_dir)
            styles.append({ 'url':nav.get_url_to(style) })
        return styles

    def get_category_for_toc(self, category):
        root_elm = E.UL(E.CLASS("toc_category"))
        # Children categories.
        nav = category.navigation
        for child in category.children:
            child_elm = E.LI(
                E.A(child.name, href=nav.get_url_to(child)),
                lxml.html.fragment_fromstring(self.get_category_for_toc(child))
            )
            root_elm.append(child_elm)

        for asset in category.assets:
            asset_elm = E.LI(
                E.A(asset.title, href="")
                # E.A(asset.title, href=nav.get_url_to(asset))
            )
            root_elm.append(asset_elm)

        root_elm = lxml.html.tostring(root_elm)
        root_elm = root_elm.decode(sys.getdefaultencoding())
        return root_elm

    def render(self):
        """Renders the templates."""
        categories_toc = self.get_category_for_toc(self.root_category)
        styles = self.get_styles_for_render(self.root_category)
        title = _('Table of Contents')
        titleimage = None   # TODO
        rendered = self.templates['template_toc'].render(
                                        language = self.language,
                                        styles = styles,
                                        title = title,
                                        titleimage = titleimage,
                                        categories_toc = categories_toc)
        utility.io.ensure_dir(self.destination_content_dir)
        rendered_path = os.path.join(self.destination_content_dir,
                                     'index.html')
        with open(rendered_path, mode='wb') as outfile:
            outfile.write(rendered.encode('utf-8'))
