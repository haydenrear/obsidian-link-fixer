import os
from pathlib import Path
from typing import Optional, Callable

import link_matcher


class FileIndex:
    def __init__(self, directory: str, filename: str, filetype: str, links: [str], size: int):
        self.directory = directory
        self.abs_path = filename
        self.filetype = filetype
        self.links = links
        self.sanitized_to_value = {}
        self.size = size

    @staticmethod
    def get_file_type(filename: str):
        files = filename.split('.')
        return files[len(files) - 1] if len(files) > 1 else 'None'

    def update_true_link(self, sanitized_link_to_update_for: str, updated: str):
        self.sanitized_to_value[sanitized_link_to_update_for] = updated

    def delete_if_empty(self):
        if self.size == 0:
            os.remove(self.abs_path)

    def get_links(self):
        return self.links

    def get_path_for_file(self):
        return self.directory

    def __str__(self):
        return f'''
            directory: {self.directory}
            filename: {self.abs_path}
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
        self.file_indices: [FileIndex] = []

    def set_true_link_for_sanitized(self, sanitized: str, path: Path):
        pass

    def find_file_by_file_name(self, filename: str) -> [FileIndex]:
        if filename in self.file_index_by_name.keys():
            return self.file_index_by_name[filename]

    def link_file_filter(self, filename: str) -> bool:
        return filename.endswith('.md')

    def find_link_ends_with(self, filename: str) -> [FileIndex]:
        for filename_found, file_index in self.file_index_by_filename:
            if filename in filename_found or filename_found in filename:
                return file_index

    def read_lines(self, index: FileIndex) -> (any, [str]):
        with open(index.abs_path, 'r+', encoding='utf-8') as file:
            try:
                return file, file.readlines()
            except Exception as e:
                print(e)
                pass

    def update_links_in_files(self, matcher: Optional[Callable[[str], bool]] = None):
        for file in iter(filter(lambda x: x.filetype == 'md', self.file_indices)):
            file: FileIndex = file
            new_lines = []
            file_found, file_lines = self.read_lines(file)
            for file_line in file_lines:
                for link in self.link_matcher.get_all_links(file_line):
                    if (matcher and matcher(link)) or not matcher:
                        if link in file.sanitized_to_value.keys():
                            link_to_switch = file.sanitized_to_value[link]
                            file_line = file_line.replace(link, link_to_switch)
                new_lines.append(file_line)
            file_found.close()
            with open(file.abs_path, 'w', encoding='utf-8') as file_to_write:
                file_to_write.writelines(new_lines)

    def get_updated_link(self, link_to_switch, updater):
        if updater is not None:
            link_to_switch = updater(link_to_switch)
        else:
            link_to_switch = link_to_switch.replace(
                '/Users/hayde/Library/Mobile Documents/iCloud~md~obsidian/Documents/Hayden/', '')
        return link_to_switch

    def delete_files(self):
        for file in self.file_indices:
            file.delete_if_empty()

    def add_file(self, directory, abs_path, filename):
        file_type = FileIndex.get_file_type(abs_path)
        file = FileIndex(directory, abs_path, file_type,
                         FileIndices.get_links(os.path.join(directory, filename), abs_path, self.link_matcher)
                         if self.link_file_filter(abs_path)
                         else [], os.path.getsize(abs_path))
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
                    returnlinks.extend(this_link_matcher.get_all_links(line))
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


class FileIndicesFactory:

    @staticmethod
    def create_file_indices(return_indices: FileIndices, path: Path) -> FileIndices:
        for (root, dirs, files) in os.walk(path):
            for file in files:
                if '.git' not in root:
                    return_indices.add_file(root, os.path.abspath(os.path.join(root, file)), file)
        return return_indices
