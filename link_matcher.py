import abc

import regex

from file_manager import *


class LinkMatcher:

    @abc.abstractmethod
    def matches(self, line: str) -> bool:
        pass

    @abc.abstractmethod
    def get_all_links(self, line: str) -> [str]:
        pass


class DelegatingLinkMatcher(LinkMatcher):

    def __init__(self):
        self.matchers = [ObsidianLinkMatcher(), MarkdownLinkMatcher()]

    def matches(self, line: str) -> bool:
        return len(list(filter(lambda x: x.matches(line), self.matchers))) != 0

    def get_all_links(self, line: str) -> [str]:
        links = []
        for m in filter(lambda m: m.matches(line), self.matchers):
            links.extend(m.get_all_links(line))
        return links


class MarkdownLinkMatcher(LinkMatcher):

    def __init__(self):
        self.regex = regex.compile('!\[.*\]\(.*\)')

    def matches(self, line: str) -> bool:
        return len(self.regex.findall(line)) != 0

    def get_all_links(self, line: str, root_dir: str = '') -> [str]:
        links = []
        found = self.regex.findall(line)
        for link_line in found:
            if '![[' in link_line:
                continue
            try:
                link = link_line.split('![')[1].split(']')[1].split('(')[1][:-1]
                print(f"Found link {link}.")
                links.append(link)
            except Exception as e:
                print(f'Failed to split link {link_line}')

        return links


class ObsidianLinkMatcher(LinkMatcher):

    def __init__(self):
        self.regex = regex.compile('!\[\[.*\]\]')

    def matches(self, line: str) -> bool:
        return len(self.regex.findall(line)) != 0

    def get_all_links(self, line: str) -> [str]:
        links = []
        for potential_link in self.regex.findall(line):
            if self.get_end() in potential_link:
                sanitized_link_found = potential_link.split(self.get_end())[0]
                links.append(sanitized_link_found)
        return links

    def get_split(self) -> str:
        return '![['

    def get_end(self) -> str:
        return ']]'

