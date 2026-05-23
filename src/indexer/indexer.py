import os
from pathlib import Path

class Indexer:
    def __init__(self, directory):
        self.directory = Path(directory)

    def update_index(self):
        index_file = self.directory / 'index.txt'
        with open(index_file, 'w') as idx:
            for item in self.directory.iterdir():
                if item.is_file() and item.suffix == '.md':
                    idx.write(f"{item.name}\n")
        print(f"Index updated at {index_file}")

    def add_file_to_index(self, file_path):
        file_path = Path(file_path)
        if file_path.exists() and file_path.suffix == '.md':
            self.update_index()
            print(f"File {file_path.name} added to index.")
        else:
            print(f"File {file_path} does not exist or is not a markdown file.")