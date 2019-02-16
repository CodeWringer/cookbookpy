import utility.io
import os
from classes.navigation_to_path import NavigationToPath

class Asset():
    """Model class that represents an asset file."""
    def __init__(self, file_path):
        self.file_path = file_path
        self.parent = None     # A Category object.
        self.navigation = None # A Navigation object.
        self.name = os.path.basename(file_path)
        self.text_content = self.get_content()
        self.title = self.get_section(_('Title'))
        self.see_also = self.get_see_also() # NavigationToPath objects.
        print('[Asset] Acquired %s see also entries for %s' % (str(len(self.see_also)), self.name))

    def get_see_also(self):
        """Returns a list of NavigationToPath objects for every entry in the seealso section."""
        lines = self.get_section(_('See Also'))
        seeAlso = []
        for line in lines:
            seeAlso.append(NavigationToPath(self, line))
        return seeAlso

    def get_content(self):
        """Loads the file contents as text from disk an returns an array of text lines."""
        return utility.io.get_file_text_lines(self.file_path, encoding='windows-1252')

    def get_section(self, section_name):
        """Returns all lines, that belong to the section with the given name.
        Parameters
        ---------
        section_name : str
            Name of the section to get.
        """
        print('[Asset] Reading section "%s"' % (section_name))
        sectionLines = []
        indexSectionStart = -1
        indexSectionEnd = -1
        # Get start and end index of section
        for line in self.text_content:
            if line.startswith('!' + section_name):
                indexSectionStart = self.text_content.index(line) + 1
            elif line.startswith('!') and indexSectionStart >= 0:
                indexSectionEnd = self.text_content.index(line)
                break
        if indexSectionStart > 0 and indexSectionEnd < 0:
            indexSectionEnd = len(self.text_content)

        # Get section
        for i in range(indexSectionStart, indexSectionEnd):
            lineContent = self.text_content[i]
            lineContent = lineContent.strip()

            # Check if line is empty string
            if not lineContent:
                continue

            sectionLines.append(lineContent)

        print('[Asset] Returning %s lines for section "%s"' % (str(len(sectionLines)), section_name))
        return sectionLines
