import os
import json
from typing import Dict, List, Tuple
from src.parser.link_parser import LinkParser

class Indexer:
    """Builds and manages an index of links between documents."""

    def __init__(self):
        self.link_parser = LinkParser()
        self.index: Dict[str, List[Tuple[str, str]]] = {}

    def build_index(self, documents: Dict[str, str]) -> None:
        """Builds the link index from document dictionary.

        Args:
            documents: Dictionary of {filename: content}
        """
        self.index = self.link_parser.parse_documents(documents)

    def build_index_from_directory(self, directory: str, file_extension: str = ".md") -> None:
        """Builds index from all files in a directory with specified extension.

        Args:
            directory: Path to directory containing documents
            file_extension: File extension to filter by (default: .md)
        """
        documents = {}
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(file_extension):
                    path = os.path.join(root, file)
                    with open(path, 'r') as f:
                        documents[file] = f.read()
        self.build_index(documents)

    def get_links(self, doc_name: str) -> List[Tuple[str, str]]:
        """Retrieves all links from a specific document.

        Args:
            doc_name: Name of the document to query

        Returns:
            List of (link_text, url) tuples
        """
        return self.index.get(doc_name, [])

    def get_all_links(self) -> Dict[str, List[Tuple[str, str]]]:
        """Returns the complete link index.

        Returns:
            Dictionary of {filename: [(link_text, url), ...]}
        """
        return self.index

    def save_index(self, output_file: str) -> None:
        """Saves the index to a JSON file.

        Args:
            output_file: Path to output JSON file
        """
        with open(output_file, 'w') as f:
            json.dump(self.index, f)

    def load_index(self, input_file: str) -> None:
        """Loads an index from a JSON file.

        Args:
            input_file: Path to input JSON file
        """
        with open(input_file, 'r') as f:
            self.index = json.load(f)