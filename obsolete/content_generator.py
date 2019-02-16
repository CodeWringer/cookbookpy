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

class ContentGenerator:
    """Core class that handles the generation of html contents"""
    def __init__(self):
        super(ContentGenerator, self).__init__()

    """Returns all lines, of the given lines list, that belong to the section with the given name"""
    def get_section(self, sectionName, lines):
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
