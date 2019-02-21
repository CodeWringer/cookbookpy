import unittest
from utility.url import get_url

class TestUtilityUrl(unittest.TestCase):
    def test_get_url_same(self):
        source_path = 'Src\\source\\abc.recipe'
        dest_path = 'Src\\source\\def.md'
        goal = 'def.md'
        url = get_url(source_path, dest_path)
        print('[test_get_url_same] ' + url)
        self.assertEqual(url, goal)

    def test_get_url_different(self):
        source_path = 'Src\\source\\ADir\\abc.recipe'
        dest_path = 'Src\\source\\OtherDir\\def.md'
        goal = '../OtherDir/def.md'
        url = get_url(source_path, dest_path)
        print('[test_get_url_different] ' + url)
        self.assertEqual(url, goal)

    def test_get_url_otherdir(self):
        source_path = 'Src\\source\\ADir\\abc.recipe'
        dest_path = 'Src\\source\\OtherDir\\ASubDir\\def.md'
        goal = '../OtherDir/ASubDir/def.md'
        url = get_url(source_path, dest_path)
        print('[test_get_url_otherdir] ' + url)
        self.assertEqual(url, goal)

    def test_get_url_adir(self):
        source_path = 'Src\\source\\OtherDir\\ASubDir\\def.md'
        dest_path = 'Src\\source\\ADir\\abc.recipe'
        goal = '../../ADir/abc.recipe'
        url = get_url(source_path, dest_path)
        print('[test_get_url_adir] ' + url)
        self.assertEqual(url, goal)
