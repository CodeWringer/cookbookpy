import sys
import os
import re
import utility.io
from classes.nav_element import NavigationElement

TYPE_RECIPE = 0,
TYPE_MARKDOWN = 1

class ContentPage():
    """Model class that represents a page of content"""
    def __init__(self, file_path, navigation_generator, template_recipe, template_markdown):
        super(ContentPage, self).__init__()
        self.file_path = file_path
        self.template_recipe = template_recipe
        self.template_markdown = template_markdown
        self.navigation_generator = navigation_generator

        reg_pattern_type_recipe = '\.recipe'
        reg_pattern_type_markdown = '\.md'

        match_type_recipe = re.match(reg_pattern_type_recipe, file_path)
        match_type_markdown = re.match(reg_pattern_type_markdown, file_path)

        if match_type_recipe is None and match_type_markdown is None:
            raise Exception("Invalid file type")
        else:
            self.text_content = utility.io.get_file_text_lines(sourceFilePath, sourceEncoding='windows-1252', targetEncoding='utf-8')
            if match_type_recipe is not None:
                self.type = TYPE_RECIPE
                determine_sections_recipe()
            elif match_type_markdown is not None:
                self.type = TYPE_MARKDOWN
                determine_sections_markdown()

    """Returns all lines, that belong to the section with the given name"""
    def get_section(self, sectionName):
        print('Reading section ' + sectionName + ' in ' + str(len(self.text_content)) + ' lines')
        sectionLines = []
        indexSectionStart = -1
        indexSectionEnd = -1
        # Get start and end index of section
        for line in self.text_content:
            if line.startswith('!' + sectionName):
                indexSectionStart = self.text_content.index(line) + 1
            elif line.startswith('!') and indexSectionStart >= 0:
                indexSectionEnd = self.text_content.index(line) - 1
                break
        if indexSectionEnd < 0:
            indexSectionEnd = len(self.text_content) - 1

        # Get section
        for i in range(indexSectionStart, indexSectionEnd + 1):
            lineContent = self.text_content[i]
            lineContent = lineContent.strip()

            # Check if line is empty string
            if not lineContent:
                continue

            sectionLines.append(lineContent)

        print('Returning ' + str(len(sectionLines)) + ' lines for section ' + sectionName)
        return sectionLines

    """Attempts to get all the sections needed for this page to represent a recipe"""
    def determine_sections_recipe(self):
        # Read file information in expected format
        self.title = get_section('Titel')[0]
        self.servings = get_section('Portionen')[0]
        self.ingredients = get_section('Zutatenliste')
        self.utensils = get_section('Utensilien')
        self.preparation = get_section('Vorbereitung')
        self.cooking = get_section('Zubereitung')

    """Attempts to get all the sections needed for this page to represent a markdown controlled page"""
    def determine_sections_markdown(self):
        self.title = get_section('Titel')[0]
        self.markdown = get_section('Markdown')

    """Returns this page of content in rendered format"""
    def get_rendered(self, template):
        nav_element = self.navigation_generator.get_for(self)
        if self.type == TYPE_RECIPE:
            ingredients = get_section_rendered(self.ingredients, 'ingredients')
            utensils = get_section_rendered(self.utensils, 'utensils')
            preparation = get_section_rendered(self.preparation, 'preparation')
            cooking = get_section_rendered(self.cooking, 'cooking')
            return self.template_recipe.render(categories=nav_element.get_categories_stepped, category=nav_element.get_category_current, title=self.title, servings=self.servings, ingredients=ingredients, utensils=utensils, preparation=preparation, cooking=cooking, article_previous=None, article_next=None)
        elif self.type == TYPE_MARKDOWN:
            return self.template_markdown.render(categories=nav_element.get_categories_stepped, category=nav_element.get_category_current, title=self.title, content=self.markdown)

    """Returns an html render of the given section lines array"""
    # TODO: Rework -> Generalize or rather use lxml/jinja2
    def get_section_rendered(self, sectionArray, cssClass=None):
        # print('Received sectionArray: ' + str(sectionArray))

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
            # print('Returning ordered list')

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
            # print('Returning unordered list')

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
            # print('Returning table')

            columnCount = 0
            for line in sectionArray:
                value = line[mTbl.end(0):]
                splits = re.split(regPatTD, value)
                if len(splits) > columnCount:
                    columnCount = len(splits)
                    # print('new columnCount: ' + str(columnCount))

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
