from classes.asset import Asset
import os
import utility.io

class AssetContent(Asset):
    """Base class for recipe/markdown assets."""
    def __init__(self, path):
        super().__init__(path)
        self.parent = None     # A Category object.
        self.title = self.get_section('Title')[0]
        self.dest_name = os.path.splitext(self.name)[0] + '.html'
        self.navigation = None # A Navigation object.
        self.see_also = self.get_see_also() # NavigationForPath objects.
        print('[Asset] Acquired %s see also entries for %s' % (str(len(self.see_also)), self.name))

    def get_see_also(self):
        """Returns a list of NavigationForPath objects for every entry in the see_also section."""
        lines = self.get_section('See Also')
        see_also = []
        for line in lines:
            pass
            # TODO
            # url = NavigationForPath(self, line)
            # see_also.append(url)
        return see_also

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
            if (line.startswith('!' + section_name) or
                line.startswith('!' + _(section_name))):
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

    def render(self, generator, dest_dir):
        """Renders and writes out this asset."""
        # Render self.
        rendered = self.get_rendered(generator)

        # Write self to destination directory.
        dest_file_path = os.path.join(dest_dir, self.dest_name)
        utility.io.ensure_dir(dest_dir)
        with open(dest_file_path, mode='wb') as outfile:
            outfile.write(rendered.encode('utf-8'))

    def get_rendered(self, generator):
        pass
