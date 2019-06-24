import os
from pathlib import Path
import unittest
from pyfakefs import fake_filesystem_unittest

from resticprofile.filesearch import FileSearch, find_configuration_file, DEFAULT_SEARCH_LOCATIONS

TEST_FILE = 'test.conf'


class TestFileSearch(fake_filesystem_unittest.TestCase):

    def setUp(self):
        self.setUpPyfakefs()
        os.makedirs(str(Path().home()), exist_ok=True)
        for path in DEFAULT_SEARCH_LOCATIONS:
            os.makedirs(path)

    def create_file(self, filename: str):
        with open(filename, 'w') as filehandle:
            filehandle.write("Fake configuration file for testing")

    def test_no_configuration_file(self):
        filepath = find_configuration_file(TEST_FILE)
        self.assertIs(None, filepath)

    def test_configuration_file_in_home_folder(self):
        test_file = str(Path(Path().home()) / TEST_FILE)
        self.create_file(test_file)
        filepath = find_configuration_file(TEST_FILE)
        self.assertEqual(test_file, filepath)

    def test_configuration_file_in_current_folder(self):
        test_file = str(Path(os.getcwd()) / TEST_FILE)
        self.create_file(test_file)
        filepath = find_configuration_file(TEST_FILE)
        self.assertEqual(test_file, filepath)

    def test_configuration_file_in_default_search_locations(self):
        for path in DEFAULT_SEARCH_LOCATIONS:
            test_file = str(Path(path) / TEST_FILE)
            self.create_file(test_file)
            filepath = find_configuration_file(TEST_FILE)
            self.assertEqual(test_file, filepath)
            os.remove(test_file)


    def test_find_rooted_file(self):
        search = FileSearch('/folder')
        filepath = search.find_file('/file')
        self.assertEqual(str(Path('/file')), filepath)

    def test_find_single_file(self):
        search = FileSearch('/folder')
        filepath = search.find_file('file')
        self.assertEqual(str(Path('/folder/file')), filepath)

    def test_find_file_with_path(self):
        search = FileSearch('/folder')
        filepath = search.find_file('subfolder/file')
        self.assertEqual(str(Path('/folder/subfolder/file')), filepath)


    def test_find_rooted_dir(self):
        search = FileSearch('/folder')
        filepath = search.find_dir('/dir')
        self.assertEqual(str(Path('/dir')), filepath)

    def test_find_single_dir(self):
        search = FileSearch('/folder')
        filepath = search.find_dir('dir')
        self.assertEqual(str(Path(os.getcwd()) / 'dir'), filepath)

    def test_find_dir_with_path(self):
        search = FileSearch('/folder')
        filepath = search.find_dir('subfolder/dir')
        self.assertEqual(str(Path(os.getcwd()) / 'subfolder/dir'), filepath)
