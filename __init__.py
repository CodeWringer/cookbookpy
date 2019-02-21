import os
import utility.io
from classes.generator import Generator
import gettext
import argparse
import unittest
from unittests.test_utility_url import TestUtilityUrl

parser = argparse.ArgumentParser()
parser.add_argument('--unittest', type=bool, default=False)
args = parser.parse_args()

if args.unittest:
    suite = unittest.TestLoader().loadTestsFromTestCase(TestUtilityUrl)
    unittest.TextTestRunner(verbosity=2).run(suite)
else:
    package_dir = os.path.dirname(__file__)
    settings_path = os.path.join(package_dir, 'settings.txt')

    if utility.io.get_file_exists(settings_path):
        lines_settings = utility.io.get_file_text_lines(settings_path, encoding='windows-1252')

    settings = {
        'source_content_dir' : None,
        'destination_content_dir' : None,
        'theme_dir' : None,
        'template_dir' : None,
        'language' : None
        }

    # Read settings.
    for line in lines_settings:
        split = line.split('=')
        setting = split[0].strip().strip('"')
        value = split[1].strip().strip('"')
        if setting in settings:
            settings[setting] = value
            print('[__init__] Acquired setting "%s" with value "%s"' % (setting, value))
        else:
            print('[__init__] Ignoring unexpected setting "%s"' % (setting))

    # Get language.
    locale_path = os.path.join(package_dir, 'locales')
    print('[__init__] locale path: %s' % (locale_path))
    if settings['language'] != None:
        lang = gettext.translation ('base', locale_path, [settings['language']] )
    else:
        lang = gettext.translation ('base', locale_path, ['en'] )
    lang.install()
    _ = lang.gettext

    # Begin process.
    Generator(settings['source_content_dir'],
            settings['destination_content_dir'],
            settings['template_dir'],
            settings['language']
            )
