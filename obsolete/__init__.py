import sys
import os
import re
import codecs
import lxml, lxml.html
from distutils.dir_util import copy_tree
from os import walk
from os.path import getmtime
from jinja2 import Template, Environment, select_autoescape, FileSystemLoader
from lxml.html import fromstring
import utility.io
import utility.url
from classes.content_page import ContentPage
from classes.content_generator import ContentGenerator
from classes.nav_generator import NavGenerator

"""Renders all templates in this file's subdirectories, using jinja2"""
def render_templates(sourcePath, outputPath):
    env = Environment(
        loader=FileSystemLoader(sourcePath, encoding='windows-1252'),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )
    nav_generator = NavGenerator(sourcePath)
    content_generator = ContentGenerator()

    # Read base templates
    baseTemplate = env.get_template('base.html')
    baseRecipeTemplate = env.get_template('baseRecipe.html')
    baseIndexTemplate = env.get_template('baseIndex.html')
    homeTemplate = env.get_template('home.html')

    # Get subdirectories
    dirNames = utility.io.get_directory_names(sourcePath)

    # Create output directory, if necessary
    utility.io.ensure_dir(outputPath)

    categories = nav_generator.categories
    outputHomePath = os.path.join(outputPath, 'index.html')

    homeTemplateRendered = homeTemplate.render(categories=categories, title='Rezeptbuch')
    # Write template to output directory
    with open(outputHomePath, mode='wb') as outfile:
        outfile.write(homeTemplateRendered.encode('utf-8'))

    # Iterate subdirectories
    # Create subdirectory in output directory, if necessary
    for dirName in dirNames:
        outputDirPath = os.path.join(outputPath, dirName)
        sourceDirPath = os.path.join(sourcePath, dirName)
        utility.io.ensure_dir(outputDirPath)
        outputIndexPath = os.path.join(outputDirPath, 'index.html')

        # Copy theme directory contents
        if dirName == 'theme':
            copy_tree(sourceDirPath, outputDirPath)
            continue

        sourceDir = os.path.basename(os.path.normpath(sourcePath))
        steps = utility.url.get_relative_steps(sourceDir, sourceDirPath)
        categoriesStepped = nav_generator.get_stepped_categories(steps)
        fileNames = utility.io.get_file_names(sourceDirPath)

        categoryCurrent = None

        # Render index.html for current category
        for category in categoriesStepped:
            if category.name == dirName:
                categoryCurrent = category
                break

        baseIndexTemplateRendered = baseIndexTemplate.render(categories=categoriesStepped, category=categoryCurrent, title='Inhaltsverzeichnis')
        # Write template to output directory
        with open(outputIndexPath, mode='wb') as outfile:
            outfile.write(baseIndexTemplateRendered.encode('utf-8'))

        # Iterate files
        for fileName in fileNames:
            fileNamesNoExt = os.path.splitext(fileName)[0]
            sourceFilePath = os.path.join(sourceDirPath, fileName)
            outFilePath = os.path.join(outputDirPath, fileNamesNoExt + '.html')

            # Read source file
            lines = utility.io.get_file_text_lines(sourceFilePath, sourceEncoding='windows-1252', targetEncoding='utf-8')

            # Read file information in expected format
            title = content_generator.get_section('Titel', lines)[0]
            servings = content_generator.get_section('Portionen', lines)[0]

            ingredients = content_generator.get_section('Zutatenliste', lines)
            ingredients = content_generator.get_section_rendered(ingredients, 'ingredients')

            utensils = content_generator.get_section('Utensilien', lines)
            utensils = content_generator.get_section_rendered(utensils, 'utensils')
            
            preparation = content_generator.get_section('Vorbereitung', lines)
            preparation = content_generator.get_section_rendered(preparation, 'preparation')
            
            cooking = content_generator.get_section('Zubereitung', lines)
            cooking = content_generator.get_section_rendered(cooking, 'cooking')

            # Render template
            baseRecipeTemplateRendered = baseRecipeTemplate.render(categories=categoriesStepped, category=categoryCurrent, title=title, servings=servings, ingredients=ingredients, utensils=utensils, preparation=preparation, cooking=cooking, article_previous=None, article_next=None)

            # Write template to output directory
            with open(outFilePath, mode='wb') as outfile:
                outfile.write(baseRecipeTemplateRendered.encode('utf-8'))