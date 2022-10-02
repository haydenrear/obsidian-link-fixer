import abc
import file_manager
import os
from pathlib import Path
import link_fix


class LinkMatcher:
    @abc.abstractmethod
    def matches(self, line: str) -> bool:
        pass

    @abc.abstractmethod
    def get_all_links(self, line: str, links: dict[str, str], abs_path: str = '') -> [str]:
        pass

    @abc.abstractmethod
    def get_split(self) -> str:
        pass


# class MarkdownLinkMatcher(LinkMatcher):
#     def matches(self, line: str) -> bool:
#         pass
#
#     def get_all_links(self, line: str, root_dir: str = '') -> [str]:
#         pass
#
#     def get_split(self) -> str:
#         pass


class ObsidianLinkMatcher(LinkMatcher):

    def __init__(self, file_manager: file_manager.FileManager):
        self.file_manager = file_manager

    def matches(self, line: str) -> bool:
        return self.get_split() in line and self.get_end() in line

    def get_all_links(self, line: str, abs_path: str = '') -> [str]:
        path = Path(abs_path)
        parent_name = path.parent.name
        links = []
        for potential_link in line.split(self.get_split()):
            if self.get_end() in potential_link:
                sanitized_link_found = self.sanitize_link(potential_link.split(self.get_end())[0])
                links.append(sanitized_link_found)
        return links

    def get_split(self) -> str:
        return '![['

    def get_end(self) -> str:
        return ']]'

    def sanitize_link(self, link: str) -> str:
        print(f'pre-sanitized: {link}\n')
        return link

