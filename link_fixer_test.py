import os
import shutil
import unittest

import link_builder
from file_manager import FileManager
from file_index import *
from link_fixer import LinkFixer
from link_matcher import ObsidianLinkMatcher, DelegatingLinkMatcher


def try_remove(file):
    try:
        if os.path.isfile(file):
            os.remove(file)
        elif os.path.isdir(file):
            os.removedirs(file)
    except Exception as e:
        print(e)


def delete_files_and_dirs_recursively(file_or_dir: str):
    if os.path.isdir(file_or_dir):
        for file_dir in os.listdir(file_or_dir):
            delete_files_and_dirs_recursively(os.path.join(file_or_dir, file_dir))
        try:
            try_remove(file_or_dir)
        except Exception as e:
            print(f"Failed to delete {file_or_dir} with error: {e}")
    elif os.path.isfile(file_or_dir):
        try_remove(file_or_dir)


class MyTestCase(unittest.TestCase):

    # def setUp(self):
    #     self.remove_test_files()
    #     shutil.copytree('./test_files', './test_files_test')
    #
    # def tearDown(self):
    #     self.remove_test_files()

    def test_link_matcher_report(self):
        test_file_indices = FileIndices(DelegatingLinkMatcher())
        file_indices = FileIndicesFactory.create_file_indices(test_file_indices, Path('../'))
        link_builder_found = link_builder.LinkFixEngine(file_indices, FileManager(),
                                                        link_builder.DelegatingSimilarityScoreEngine())
        # link_builder_found.get_true_links()
        link_builder_found.write_link_report()

        # print('updated links!')
        #
        # test_file_indices.update_links_in_files()

        # test_file_indices.delete_files()

    def test_get_true_links(self):
        test_file_indices = self.test_file_indices()
        link_builder_found = link_builder.LinkFixEngine(test_file_indices, FileManager(),
                                                        link_builder.DelegatingSimilarityScoreEngine())
        link_builder_found.get_true_links()
        assert len(test_file_indices.file_indices) != 0
        for test_file_index in test_file_indices.file_indices:
            if test_file_index.filetype == 'md':
                if len(test_file_index.links):
                    value = test_file_index.sanitized_to_value
                    print(value)

    def test_update_links(self):
        test_file_indices = self.test_file_indices()
        link_builder_found = link_builder.LinkFixEngine(test_file_indices, FileManager(),
                                                        link_builder.DelegatingSimilarityScoreEngine())
        link_builder_found.get_true_links()
        test_file_indices.update_links_in_files(self.link_update_condition(os.path.dirname(__file__)))
        with open(os.path.join('test_files_test', 'Architecture.md'), 'r') as a:
            assert 'link-fixer/test_files_test/pngs/IMG_1345.png' in ''.join(a.readlines())
        test_file_indices.delete_files()

    def link_update_condition(self, relative_to):
        return lambda f: self.path_exists(f, relative_to)

    def path_exists(self, f, relative_to):
        does_path_exists = not os.path.exists(os.path.relpath(f, relative_to))
        return does_path_exists


    def test_get_links(self):
        indices = self.test_file_indices()
        for f in [i for j in indices.file_index_by_filename.values()
                  for i in j]:
            f: FileIndex = f
            if len(f.links) != 0:
                print(f.links)

    def remove_test_files(self):
        delete_files_and_dirs_recursively('./test_files_test')

    def test_split_link(self):
        obsidian_link_matcher = ObsidianLinkMatcher()
        link = obsidian_link_matcher.get_all_links('dsfsdf![[hello]]dfsdfsd')
        assert link[0] == 'hello'
        link = obsidian_link_matcher.get_all_links('dsfsdf![[hello]]![[whatever]]dsfdef![[okay]]dfsdfsd')
        assert link == ['hello', 'whatever', 'okay']

    @staticmethod
    def test_file_indices() -> FileIndices:
        test_file_indices = FileIndices(DelegatingLinkMatcher())
        return FileIndicesFactory.create_file_indices(test_file_indices, Path('./test_files_test'))


if __name__ == '__main__':
    unittest.main()
