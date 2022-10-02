import os


class FileManager:

    def __init__(self):
        self.missing_files = []
        self.not_missing = []

    @staticmethod
    def is_file_existing(file) -> bool:
        return os.path.exists(file)

    def add_missing(self, file):
        print(f'missing file: {file}')
        self.missing_files.append(file)

    def add_not_missing(self, sanitized_link_found):
        self.not_missing.append(sanitized_link_found)