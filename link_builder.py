import pathlib
import file_manager
import os
from pathlib import Path
import link_fix


class LinkBuilder:
    def __init__(self, file_indices: link_fix.FileIndices, file_manager: file_manager.FileManager):
        self.true_links: dict[link_fix.FileIndex, list[pathlib.Path]] = {}
        self.file_indices = file_indices
        self.file_manager = file_manager

    def get_true_link(self, file_indices: link_fix.FileIndex) -> str:
        for sanitized_link_found in file_indices.links:
            path = Path(sanitized_link_found)
            is_existing = False
            file_found_name = path.name
            parent = path.parent
            parent_name = parent.name
            file_found = self.file_indices.find_file_by_file_name(file_found_name)
            while not is_existing and parent_name is not '' and file_found is not None:
                join = os.path.join(parent, sanitized_link_found)
                if file_manager.FileManager.is_file_existing(join):
                    self.file_manager.add_not_missing(sanitized_link_found)
                    return os.path.abspath(join)
                path = Path(parent)
                parent = path.parent
                parent_name = parent.name
            if file_found is not None:
                if len(file_found) != 0:
                    print(file_found)
                if len(file_found) > 1:
                    print(file_found)

    def get_true_links(self):
        for file_indice in self.file_indices.file_indices:
            self.get_true_link(file_indice)