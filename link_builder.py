import abc
import pathlib
from difflib import SequenceMatcher

import spacy

import file_manager
from file_index import *


class SimilarityScoreEngine:
    @abc.abstractmethod
    def get_score(self, file1: str, file2: str) -> float:
        pass


class SpacySimilarityScoreEngine(SimilarityScoreEngine):
    def __init__(self):
        self.nlp = spacy.load('en_core_web_lg')

    def get_score(self, file1: str, file2: str) -> float:
        one = self.nlp(file1)
        two = self.nlp(file2)
        return one.similarity(two)


class DifflibSimilarityScoreEngine(SimilarityScoreEngine):

    def get_score(self, file1: str, file2: str) -> float:
        return SequenceMatcher(None, file1, file2).ratio()


class DelegatingSimilarityScoreEngine(SimilarityScoreEngine):

    def __init__(self):
        self.spacy = SpacySimilarityScoreEngine()
        self.sequence = DifflibSimilarityScoreEngine()

    def get_score(self, file1: str, file2: str) -> float:
        one = self.spacy.get_score(file1, file2)
        two = self.sequence.get_score(file1, file2)
        return (one + two) / 2


class LinkFixEngine:
    def __init__(self, file_indices: FileIndices, file_manager: file_manager.FileManager,
                 scorer: SimilarityScoreEngine):
        self.true_links: dict[FileIndex, list[pathlib.Path]] = {}
        self.file_indices = file_indices
        self.file_manager = file_manager
        self.similarity = scorer

    def set_true_links_for_this_index(self, file_index: FileIndex):
        for sanitized_link_found in file_index.links:

            path = Path(sanitized_link_found)
            file_found_name = path.name
            file_found: [FileIndex] = self.file_indices.find_file_by_file_name(file_found_name)

            if file_found is not None:
                if len(file_found) == 1:
                    print(f'updating link for {file_found}')
                    file_index.update_true_link(sanitized_link_found, file_found[0].abs_path)
                    continue
                elif len(file_found) > 1:
                    max_map = self.get_similarity_scores(file_found, sanitized_link_found)
                    print(f'found max for {file_found}: {max_map}')

                    if len(max_map) > 1:
                        print(f"Two files contain same similarity index for {sanitized_link_found}, "
                              f"selecting the first.")
                        file_index.update_true_link(sanitized_link_found, next(iter(max_map)).abs_path)
                    elif len(max_map) == 1:
                        file_index.update_true_link(sanitized_link_found, next(iter(max_map)).abs_path)
                    else:
                        print(f"Max map did not contain any {file_found} when there existed a file.")

    def get_similarity_scores(self, file_found, sanitized_link_found):
        file_found_to_score = {}
        for each_file_found in file_found:
            file_found_to_score[each_file_found] = self.similarity.get_score(
                each_file_found.get_path_for_file(),
                sanitized_link_found
            )
        max_value = max(file_found_to_score.values())
        max_map = {k: v for k, v in file_found_to_score.items()
                   if file_found_to_score[k] == max_value}
        return max_map

    def get_true_links(self):
        for file_index_found in filter(lambda x: x.filetype == 'md', self.file_indices.file_indices):
            print(f'updating link for {file_index_found}')
            self.set_true_links_for_this_index(file_index_found)

    def write_link_report(self):
        with open('./link_report.md', 'w') as links_report:
            for file_index_found in filter(lambda x: x.filetype == 'md', self.file_indices.file_indices):
                file_index_found: FileIndex = file_index_found
                if len(file_index_found.links) != 0:
                    links_report.write(f'\nLinks for {file_index_found.abs_path}:\n\n\n')
                    for v in file_index_found.links:
                        links_report.write(f'    {v}\n')
                    links_report.write(f'Broken links:\n\n')
                    for v in file_index_found.links:
                        if not v.startswith('https'):
                            if not os.path.isabs(v):
                                v = os.path.relpath(
                                    v,'/Users/hayde/Library/Mobile Documents/iCloud~md~obsidian/Documents/Hayden')
                            if not os.path.exists(v):
                                links_report.write(f'    {v}')
                    links_report.write(f'Internet links:\n\n')
                    for v in file_index_found.links:
                        if v.startswith('https'):
                            links_report.write(f'    {v}\n')
