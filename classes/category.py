import os
import utility.io
import re
from classes.asset_recipe import AssetRecipe
from classes.asset_markdown import AssetMarkdown

class Category():
    """Represents a category."""
    def __init__(self, dir_path):
        self.dir_path = dir_path
        self.parent = None     # A Category object.
        self.navigation = None # A Navigation object.
        self.name = os.path.basename(dir_path)
        self.assets = self.get_assets()
        self.children = self.get_children() # sub-categories

    def get_assets(self):
        """Loads all assets of this category and returns them as a list."""
        pattern_markdown = '\.?(md|mdown|markdown|markdn)'
        pattern_recipe = '\.?(recipe|rp)'
        re_markdown = re.compile(pattern_markdown, re.IGNORECASE)
        re_recipe = re.compile(pattern_recipe, re.IGNORECASE)
        assets = []
        fileNames = utility.io.get_file_names(self.dir_path)
        print('[Category] Found %s files for category "%s"' % (str(len(fileNames)), self.name))
        for fileName in fileNames:
            filePath = os.path.join(self.dir_path, fileName)
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
        dirNames = utility.io.get_directory_names(self.dir_path)
        categories = []
        ignore = ['theme', 'template']
        for dirName in dirNames:
            if dirName in ignore:
                continue
            else:
                print('[Category] Processing category "%s"' % (dirName))
                category_path = os.path.join(self.dir_path, dirName)
                child = Category(category_path)
                categories.append(child)
                child.parent = self
        return categories
