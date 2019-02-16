import sys
import os
import codecs
import lxml, lxml.html
from distutils.dir_util import copy_tree
from os import walk
from os.path import getmtime
from jinja2 import Template, Environment, select_autoescape, FileSystemLoader
from lxml.html import fromstring
from classes.content_generator import ContentGenerator
from classes.nav_element import NavigationElement
import utility.io
import utility.url

class NavGenerator:
    """Core class that handles the generation of navigation elements"""
    def __init__(self, source_dir_path):
        super(NavGenerator, self).__init__()
        self.source_dir_path = source_dir_path
        self.categories = []
        self.get_categories()

    """Returns a list of categories, based on the given source directory"""
    def get_categories(self):
        url = 'index.html'
        self.categories.append(NavigationElement(url, 'Start'))
        content_generator = ContentGenerator()

        # Get sub directories for categories
        sub_dirs = utility.io.get_directory_names(self.source_dir_path)
        for sub_dir in sub_dirs:
            if sub_dir == 'theme':
                continue

            sub_dir_path = os.path.join(self.source_dir_path, sub_dir)
            children = []

            # Get file names for children
            file_names = utility.io.get_file_names(sub_dir_path)
            for file_name in file_names:
                file_name_no_extension = os.path.splitext(file_name)[0]
                file_path = os.path.join(sub_dir_path, file_name)
                title = ''

                lines = utility.io.get_file_text_lines(file_path, sourceEncoding='windows-1252', targetEncoding='utf-8')

                # Read file information in expected format
                title = content_generator.get_section('Titel', lines)[0]

                url = sub_dir + '/' + file_name_no_extension + '.html'
                children.append(NavigationElement(url, title))

            url = sub_dir + '/index.html'
            self.categories.append(NavigationElement(url, sub_dir, children))

    """Returns a category with the given count of added relative look ups"""
    def get_stepped_category(self, category, steps):
        url = utility.url.get_relative_url_stepped(steps) + category.url
        name = category.name
        childrenNew = self.get_stepped_categories(category.children, steps)
        newCategory = NavigationElement(url, name, childrenNew)
        return newCategory

    """Returns the given list of categories with the given count of added relative look ups"""
    def get_stepped_categories(self, steps):
        categoriesNew = []
        for category in self.categories:
            categoriesNew.append(self.get_stepped_category(category, steps))
        return categoriesNew