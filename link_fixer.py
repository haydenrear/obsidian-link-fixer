import os
from pathlib import Path

import file_manager
import link_matcher

from file_index import FileIndices, FileIndicesFactory
from link_builder import LinkFixEngine, DelegatingSimilarityScoreEngine


class LinkFixer:
    def __init__(self):
        self.file_manager = file_manager.FileManager()
        self.file_indices = FileIndices(link_matcher.DelegatingLinkMatcher())

    def index_files_update_links(self, directory: str):
        os.chdir(directory)
        self.get_file_index(os.curdir)
        self.print_missing()
        builder = LinkFixEngine(self.file_indices, self.file_manager, DelegatingSimilarityScoreEngine())
        builder.get_true_links()

    def update_links_in_files(self):
        for index in self.file_indices.file_indices:
            index.update_file_with_new_links()

    def get_file_index(self, directory: str):
        return FileIndicesFactory.create_file_indices(self.file_indices, Path(directory))

    def print_missing(self):
        [print(file) for file in self.file_manager.missing_files]

    def print_not_missing(self):
        [print(file) for file in self.file_manager.not_missing]
