import re
from typing import List, Dict, Tuple

class LinkParser:
    """Extracts markdown links from text with robust pattern matching."""

    def __init__(self):
        self.link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')

    def parse_links(self, text: str) -> List[Tuple[str, str]]:
        """Extracts markdown links with both text and URL.

        Args:
            text: Input markdown text to parse

        Returns:
            List of tuples containing (link_text, url)
        """
        return [(match.group(1), match.group(2)) for match in self.link_pattern.finditer(text)]

    def parse_documents(self, documents: Dict[str, str]) -> Dict[str, List[Tuple[str, str]]]:
        """Parses multiple documents and extracts links from each.

        Args:
            documents: Dictionary of {filename: content}

        Returns:
            Dictionary of {filename: [(link_text, url), ...]}
        """
        return {name: self.parse_links(content) for name, content in documents.items()}