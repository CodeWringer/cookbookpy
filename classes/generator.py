import jinja2
from jinja2 import FileSystemLoader, select_autoescape
import os
import utility.io
from classes.category import Category
from classes.navigation_to_obj import NavigationToObj
from classes.navigation_to_path import NavigationToPath

class Generator():
    """Core class that generates the cook book."""
    def __init__(self,
                 source_content_dir,
                 destination_content_dir,
                 theme_dir,
                 template_dir
                 ):
        if source_content_dir == None:
            raise ValueError('source_content_dir must not be None!')
        if destination_content_dir == None:
            raise ValueError('destination_content_dir must not be None!')
        self.source_content_dir = source_content_dir
        self.destination_content_dir = destination_content_dir
        self.theme_dir = theme_dir
        self.template_dir = template_dir
        print('--------- [Generator] Getting templates')
        self.templates = self.get_templates()
        print('[Generator] Acquired %s templates' % (str(len(self.templates))))
        print('--------- [Generator] Getting categories')
        self.root_category = Category(self.source_content_dir)
        print('--------- [Generator] Getting navigation')
        NavigationToObj(self.root_category)
        self.render()

    def get_templates(self):
        """Loads and returns the template files."""
        templatePath = os.path.join(self.source_content_dir, self.template_dir)
        env = jinja2.Environment(
            loader=FileSystemLoader(templatePath,
                                    encoding='windows-1252'),
            autoescape=select_autoescape(['html', 'xml']),
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

    def render(self):
        """Renders the templates."""
        pass
