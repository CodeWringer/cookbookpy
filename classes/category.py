import os
import utility.io
import re
import sys
from classes.asset_recipe import AssetRecipe
from classes.asset_markdown import AssetMarkdown
from lxml.html import builder as E
import lxml
from utility.url import get_url
from utility.io import get_new_ext

class Category():
    """Represents a category."""
    def __init__(self, path):
        self.path = path
        self.file_path = os.path.join(self.path, 'index.html')
        self.parent = None     # A Category object.
        self.navigation = None # A Navigation object.
        self.name = os.path.basename(path)
        self.assets = self.get_assets()
        self.children = self.get_children() # sub-categories

    def get_assets(self):
        """Loads all assets of this category and returns them as a list."""
        pattern_markdown = '\.?(md|mdown|markdown|markdn)'
        pattern_recipe = '\.?(recipe|rp)'
        re_markdown = re.compile(pattern_markdown, re.IGNORECASE)
        re_recipe = re.compile(pattern_recipe, re.IGNORECASE)
        assets = []
        fileNames = utility.io.get_file_names(self.path)
        print('[Category] Found %s files for category "%s"' % (str(len(fileNames)), self.name))
        for fileName in fileNames:
            filePath = os.path.join(self.path, fileName)
            print('[Category] Processing file "%s"' % (fileName))
            split = fileName.split('.')
            extension = split[1]
            if re_markdown.match(extension) != None:
                print('[Category] As markdown')
                recipe = AssetMarkdown(filePath)
                assets.append(recipe)
                recipe.parent = self
            elif re_recipe.match(extension) != None:
                print('[Category] As recipe')
                recipe = AssetRecipe(filePath)
                assets.append(recipe)
                recipe.parent = self
        return assets

    def get_children(self):
        """Loads all children categories of this category and returns them as a list."""
        dirNames = utility.io.get_directory_names(self.path)
        categories = []
        ignore = ['theme', 'template']
        for dirName in dirNames:
            if dirName in ignore:
                continue
            else:
                print('[Category] Processing category "%s"' % (dirName))
                category_path = os.path.join(self.path, dirName)
                child = Category(category_path)
                categories.append(child)
                child.parent = self
        return categories

    def render(self, generator, dest_dir):
        """Renders and writes out this category, including its children and assets."""
        # Render self.
        rendered = self.get_rendered(generator)

        # Write self to destination directory.
        dest_dir_path = os.path.join(dest_dir, self.name)
        dest_file_path = os.path.join(dest_dir_path, 'index.html')
        utility.io.ensure_dir(dest_dir_path)
        with open(dest_file_path, mode='wb') as outfile:
            outfile.write(rendered.encode('utf-8'))

        # Have assets render themselves.
        for asset in self.assets:
            asset.render(generator, dest_dir_path)

        # Have children render themselves.
        for child in self.children:
            child.render(generator, dest_dir_path)

    def get_rendered(self, generator):
        """Returns an html representation of this category.
        Parameters
        ---------
        generator : Generator
          The generator object this category belongs to.
        """
        categories_toc = self.get_rendered_for_toc()
        categories_toc = lxml.html.tostring(categories_toc, pretty_print=True)
        categories_toc = categories_toc.decode(sys.getdefaultencoding())
        title = self.name
        titleimage = None # TODO

        categories = []
        for category in generator.root_category.children:
            categories.append({ 'name': category.name,
                                'url': get_url(self.file_path,
                                               category.file_path) })

        neighbor_previous = None
        neighbor_next = None
        if len(self.navigation.neighbors_prev) > 0:
            neighbor = self.navigation.neighbors_prev[0]
            neighbor_previous = {
                'title': neighbor.name,
                'url': get_url(self.file_path,
                               neighbor.file_path)
            }
        if len(self.navigation.neighbors_next) > 0:
            neighbor = self.navigation.neighbors_next[0]
            neighbor_next = {
                'title': neighbor.name,
                'url': get_url(self.file_path,
                               neighbor.file_path)
            }

        rendered = generator.templates['template_category'].render(
            language = generator.language,
            styles = generator.get_style_urls(self),
            categories_toc = categories_toc,
            categories = categories,
            title = title,
            titleimage = titleimage,
            neighbor_previous = neighbor_previous,
            neighbor_next = neighbor_next
        )
        return rendered

    def get_rendered_for_toc(self, path_override=None):
        """Returns an html 'ul' element, that represents the entire table of contents for this category.
        Parameters
        ---------
        path_override : str
          If not None, gets urls for this path. Intended for use by parent categories getting the toc of their children.
        """
        root_elm = E.UL(E.CLASS("toc_category"))
        # Children categories.
        nav = self.navigation
        for child in self.children:
            if path_override != None:
                child_path = get_url(path_override, child.file_path)
            else:
                child_path = get_url(self.file_path, child.file_path)

            child_elm = E.LI(
                E.A(child.name, href=child_path),
                child.get_rendered_for_toc(path_override=self.path)
            )
            root_elm.append(child_elm)
        # Assets.
        for asset in self.assets:
            asset_path = get_new_ext(asset.path, 'html')
            if path_override != None:
                asset_path = get_url(path_override, asset_path)
            else:
                asset_path = get_url(self.file_path, asset_path)
            asset_elm = E.LI(
                E.A(asset.title, href=asset_path)
            )
            root_elm.append(asset_elm)
        return root_elm
