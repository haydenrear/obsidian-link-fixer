import os
import pathlib

import link_matcher
import file_manager
from pathlib import Path


class FileIndex:
    def __init__(self, directory: str, filename: str, filetype: str, links: [str]):
        self.directory = directory
        self.filename = filename
        self.filetype = filetype
        self.links = links

    @staticmethod
    def get_file_type(filename: str):
        files = filename.split('.')
        return files[len(files) - 1] if len(files) > 1 else 'None'

    def __str__(self):
        return f'''
            directory: {self.directory}
            filename: {self.filename}
            filetype: {self.filetype}
            links: {self.links}
        '''


# TODO: make this abstract class, and have different types of file indices.
class FileIndices:
    def __init__(self, matcher: link_matcher.LinkMatcher):
        self.file_index_by_directory = {}
        self.file_index_by_filename = {}
        self.file_index_by_name = {}
        self.file_index_by_filetype = {}
        self.link_matcher = matcher
        self.file_indices = []

    def find_file_by_file_name(self, filename: str) -> [FileIndex]:
        if filename in self.file_index_by_name.keys():
            return self.file_index_by_name[filename]

    def link_file_filter(self, filename: str) -> bool:
        return filename.endswith('.md')

    def find_link_ends_with(self, filename: str) -> [FileIndex]:
        for filename_found, file_index in self.file_index_by_filename:
            if filename in filename_found or filename_found in filename:
                return file_index

    def add_file(self, directory, abs_path, filename):
        file_type = FileIndex.get_file_type(abs_path)
        file = FileIndex(directory, abs_path, file_type,
                         FileIndices.get_links(os.path.join(directory, filename), abs_path, self.link_matcher)
                         if self.link_file_filter(abs_path)
                         else [])
        FileIndices.instantiate_add(self.file_index_by_filetype, file_type, file)
        FileIndices.instantiate_add(self.file_index_by_filename, abs_path, file)
        FileIndices.instantiate_add(self.file_index_by_directory, directory, file)
        FileIndices.instantiate_add(self.file_index_by_name, Path(abs_path).name, file)
        self.file_indices.append(file)
        return file

    @staticmethod
    def get_links(filename: str, abs_path: str, this_link_matcher: link_matcher.LinkMatcher) -> [str]:
        returnlinks = []
        try:
            with open(filename, 'r', encoding='utf-8') as read_file:
                for line in read_file:
                    returnlinks.extend(this_link_matcher.get_all_links(line, abs_path))
            return returnlinks
        except FileNotFoundError as f:
            print(f'could not find file with name {filename}')

    @staticmethod
    def instantiate_add(dictionary: dict[str, list[FileIndex]], key: str, value: FileIndex):
        try:
            dictionary[key].append(value)
        except KeyError as k:
            dictionary[key] = []
            dictionary[key].append(value)

class LinkFixer:
    def __init__(self):
        self.file_manager = file_manager.FileManager()
        self.file_indices = FileIndices(link_matcher.ObsidianLinkMatcher(self.file_manager))

    def get_file_index(self, directory: str):
        for (root, dirs, files) in os.walk(directory):
            for file in files:
                if '.git' not in root:
                    print(self.file_indices.add_file(root, os.path.abspath(file), file))

    def find_links(self):
        pass

    def fix_links(self, linked_file):
        pass

    def print_missing(self):
        [print(file) for file in self.file_manager.missing_files]

    def print_not_missing(self):
        [print(file) for file in self.file_manager.not_missing]

