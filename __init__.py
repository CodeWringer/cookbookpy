import os
import utility.io
from classes.generator import Generator
import gettext

packageDir = os.path.dirname(__file__)
settingsPath = os.path.join(packageDir, 'settings.txt')

if utility.io.get_file_exists(settingsPath):
    lines_settings = utility.io.get_file_text_lines(settingsPath, encoding='windows-1252')

settings = {
    'source_content_dir' : None,
    'destination_content_dir' : None,
    'theme_dir' : 'theme',
    'template_dir' : 'template',
    'language' : None
    }

# Read settings.
for line in lines_settings:
    split = line.split('=')
    setting = split[0].strip().strip('"')
    value = split[1].strip().strip('"')
    if setting in settings:
        settings[setting] = value
        print('[__init__] Acquired setting "'+setting+'" with value "'+value+'"')
    else:
        print('[__init__] Ignoring unexpected setting "'+setting+'"')

# Get language.
localePath = os.path.join(packageDir, 'locales')
print('[__init__] locale path: %s' % (localePath))
if settings['language'] != None:
    lang = gettext.translation ('base', localePath, [settings['language']] )
else:
    lang = gettext.translation ('base', localePath, ['en'] )
lang.install()
_ = lang.gettext

# Begin process.
Generator(settings['source_content_dir'],
        settings['destination_content_dir'],
        settings['theme_dir'],
        settings['template_dir']
        )
