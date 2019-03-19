import os
import utility.io
from classes.generator import Generator
import gettext
import argparse
import unittest
import logging
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

    # Setup logging.
    log_name = 'log.txt'
    log_file = os.path.join(package_dir, log_name)
    if utility.io.get_file_exists(log_file):
        os.remove(log_file)

    logging.basicConfig(filename=log_file,
                        filemode='a',
                        format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                        datefmt='%H:%M:%S',
                        level=logging.DEBUG)

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
            logging.info('[__init__] Acquired setting "%s" with value "%s"' % (setting, value))
        else:
            logging.info('[__init__] Ignoring unexpected setting "%s"' % (setting))

    # Get language.
    locale_path = os.path.join(package_dir, 'locales')
    logging.info('[__init__] locale path: %s' % (locale_path))
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
