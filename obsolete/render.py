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

class NavigationElement:
    """Class to represent a navigation element"""
    def __init__(self, url, name, children=None):
        self.url = url
        self.name = name
        if children == None:
            self.children = []
        else:
            self.children = children
    def __str__(self):
        return self.url + ', ' + self.name

"""Returns the names of all the sub directories in the given directory"""
def get_directory_names(directory):
    return [name for name in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, name))]

"""Returns the names of all the files in the given directory"""
def get_file_names(directory):
    f = []
    for (dirpath, dirnames, filenames) in walk(directory):
        f.extend(filenames)
        break
    return f

"""Creates the full directory path to the given directory, if it doesn't exist"""
def ensure_dir(directory):
    print('Ensuring directory ' + directory)
    if not os.path.exists(directory):
        os.makedirs(directory)

"""Returns all lines, of the given lines list, that belong to the section with the given name"""
def get_section(sectionName, lines):
    print('Reading section ' + sectionName + ' in ' + str(len(lines)) + ' lines')
    sectionLines = []
    indexSectionStart = -1
    indexSectionEnd = -1
    # Get start and end index of section
    for line in lines:
        if line.startswith('!' + sectionName):
            indexSectionStart = lines.index(line) + 1
        elif line.startswith('!') and indexSectionStart >= 0:
            indexSectionEnd = lines.index(line) - 1
            break
    if indexSectionEnd < 0:
        indexSectionEnd = len(lines) - 1

    # Get section
    for i in range(indexSectionStart, indexSectionEnd + 1):
        lineContent = lines[i]
        lineContent = lineContent.strip()

        # Check if line is empty string
        if not lineContent:
            continue

        sectionLines.append(lineContent)

    print('Returning ' + str(len(sectionLines)) + ' lines for section ' + sectionName)
    return sectionLines

"""Returns an html render of the given section lines array"""
def get_section_rendered(sectionArray, cssClass=None):
    print('Received sectionArray: ' + str(sectionArray))

    element = ''
    line = sectionArray[0]
    lineCount = 0

    regPatOl = '^\s*(?:([0-9]+\.)|\\+)\s*'
    regPatUl = '^\s*(?:\\*|-)+\s*'
    regPatTbl = '^\s*(?:\\|)+\s*'
    regPatTD = '\s*(?:\\|)+\s*'

    mOl = re.match(regPatOl, line)
    mUl = re.match(regPatUl, line)
    mTbl = re.match(regPatTbl, line)

    if mOl is not None:
        print('Returning ordered list')

        element = '<ol'
        if cssClass is not None:
            element += ' class="' + cssClass+'"'
        element += '>\n'
        for line in sectionArray:
            value = line[mOl.end(0):]
            item = '<li'
            if cssClass is not None:
                item += ' class="' + cssClass+'"'
            item += '>'
            item += value
            item += '</li>\n'
            element += item
        element += '</ol>\n'

    elif mUl is not None:
        print('Returning unordered list')

        element = '<ul'
        if cssClass is not None:
            element += ' class="' + cssClass+'"'
        element += '>\n'
        for line in sectionArray:
            value = line[mUl.end(0):]
            item = '<li'
            if cssClass is not None:
                item += ' class="' + cssClass+'"'
            item += '>'
            item += value
            item += '</li>\n'
            element += item
        element += '</ul>\n'

    elif mTbl is not None:
        print('Returning table')

        columnCount = 0
        for line in sectionArray:
            value = line[mTbl.end(0):]
            splits = re.split(regPatTD, value)
            if len(splits) > columnCount:
                columnCount = len(splits)
                print('new columnCount: ' + str(columnCount))

        element = '<table'
        if cssClass is not None:
            element += ' class="' + cssClass+'"'
        element += '>\n'
        for line in sectionArray:
            value = line[mTbl.end(0):]
            splits = re.split(regPatTD, value)

            row = '<tr'
            if (lineCount % 2 > 0):
                row += ' class="odd"'
            else:
                row += ' class="even"'
            row += '>\n'

            for column in range(0, columnCount):
                split = ''

                if len(splits) > column:
                    split = splits[column]

                if lineCount > 0:
                    data = '<td'
                    data += '>'
                    data += split
                    data += '</td>\n'
                    row += data
                else:
                    data = '<th'
                    data += '>'
                    data += split
                    data += '</th>\n'
                    row += data

            row += '</tr>\n'
            element += row
            lineCount += 1
        element += '</table>\n'

    return element

"""Returns the number of steps back up the given path it takes to get to the 
given target directory name"""
def get_relative_steps(targetDirName, path):
    steps = re.split('/|\\\\', os.path.normpath(path))
    stepCount = 0;
    count = len(steps) - 1

    for step in steps:
        if step == targetDirName:
            return count - stepCount
        stepCount += 1
    return -1

"""Returns the 'move up' segment for a url for the given number of times"""
def get_relative_url_stepped(steps):
    url = ''
    for step in range(0,steps):
        url = '../' + url
    return url

"""Returns a list of categories, based on the given source directory"""
def get_categories(sourceDirPath):
    categories = []

    url = 'index.html'
    categories.append(NavigationElement(url, 'Start'))

    # Get sub directories for categories
    subDirs = get_directory_names(sourceDirPath)
    for subDir in subDirs:
        if subDir == 'theme':
            continue

        subDirPath = os.path.join(sourceDirPath, subDir)
        children = []

        # Get file names for children
        fileNames = get_file_names(subDirPath)
        for fileName in fileNames:
            fileNamesNoExt = os.path.splitext(fileName)[0]
            filePath = os.path.join(subDirPath, fileName)
            title = ''

            lines = get_file_text_lines(filePath, sourceEncoding='windows-1252', targetEncoding='utf-8')

            # Read file information in expected format
            title = get_section('Titel', lines)[0]

            url = subDir + '/' + fileNamesNoExt + '.html'
            children.append(NavigationElement(url, title))

        url = subDir + '/index.html'
        categories.append(NavigationElement(url, subDir, children))
    return categories

"""Returns a category with the given count of added relative look ups"""
def get_stepped_category(category, steps):
    url = get_relative_url_stepped(steps) + category.url
    name = category.name
    childrenNew = get_stepped_categories(category.children, steps)
    newCategory = NavigationElement(url, name, childrenNew)
    return newCategory

"""Returns the given list of categories with the given count of added relative look ups"""
def get_stepped_categories(categories, steps):
    categoriesNew = []

    for category in categories:
        categoriesNew.append(get_stepped_category(category, steps))

    return categoriesNew

def get_file_text(path, sourceEncoding, targetEncoding):
    with open(path, mode='r', encoding=sourceEncoding) as f:
        return f.read()

def get_file_text_lines(path, sourceEncoding, targetEncoding):
    lines = []

    with open(path, mode='r', encoding=sourceEncoding) as f:
        lines = f.readlines()

    return lines

"""Renders all templates in this file's subdirectories, using jinja2"""
def render_templates(sourcePath, outputPath):
    env = Environment(
        loader=FileSystemLoader(sourcePath, encoding='windows-1252'),
        autoescape=select_autoescape(['html', 'xml']),
        trim_blocks=True,
        lstrip_blocks=True
    )

    # Read base templates
    baseTemplate = env.get_template('base.html')
    baseContentTemplate = env.get_template('baseContent.html')
    baseIndexTemplate = env.get_template('baseIndex.html')
    homeTemplate = env.get_template('home.html')

    # Get subdirectories
    dirNames = get_directory_names(sourcePath)

    # Create output directory, if necessary
    ensure_dir(outputPath)

    categories = get_categories(sourcePath)
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
        ensure_dir(outputDirPath)
        outputIndexPath = os.path.join(outputDirPath, 'index.html')

        # Copy theme directory contents
        if dirName == 'theme':
            copy_tree(sourceDirPath, outputDirPath)
            continue

        sourceDir = os.path.basename(os.path.normpath(sourcePath))
        steps = get_relative_steps(sourceDir, sourceDirPath)
        categoriesStepped = get_stepped_categories(categories, steps)
        fileNames = get_file_names(sourceDirPath)

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
            lines = get_file_text_lines(sourceFilePath, sourceEncoding='windows-1252', targetEncoding='utf-8')

            # Read file information in expected format
            title = get_section('Titel', lines)[0]
            servings = get_section('Portionen', lines)[0]

            ingredients = get_section('Zutatenliste', lines)
            ingredients = get_section_rendered(ingredients, 'ingredients')
            print('ingredients: ' + str(ingredients))

            utensils = get_section('Utensilien', lines)
            utensils = get_section_rendered(utensils, 'utensils')
            
            preparation = get_section('Vorbereitung', lines)
            preparation = get_section_rendered(preparation, 'preparation')
            
            cooking = get_section('Zubereitung', lines)
            cooking = get_section_rendered(cooking, 'cooking')

            # Render template
            baseContentTemplateRendered = baseContentTemplate.render(categories=categoriesStepped, category=categoryCurrent, title=title, servings=servings, ingredients=ingredients, utensils=utensils, preparation=preparation, cooking=cooking, article_previous=None, article_next=None)

            # Write template to output directory
            with open(outFilePath, mode='wb') as outfile:
                outfile.write(baseContentTemplateRendered.encode('utf-8'))

# Do work
workingPath = os.path.dirname(os.path.realpath(__file__))
sourceDir = 'source'
outputDir = 'output'
sourcePath = os.path.join(workingPath, sourceDir)
outputPath = os.path.join(workingPath, outputDir)
render_templates(sourcePath, outputPath)