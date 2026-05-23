import os
import hashlib
from pathlib import Path

class LocalFileSync:
    def __init__(self, local_path):
        self.local_path = Path(local_path)

    def sync_files(self, source_path, target_path):
        source_path = Path(source_path)
        target_path = Path(target_path)
        
        if not source_path.exists():
            raise FileNotFoundError(f"Source path {source_path} does not exist.")
        
        if not target_path.exists():
            target_path.mkdir(parents=True, exist_ok=True)
        
        for item in source_path.iterdir():
            if item.is_file() and item.suffix == '.md':
                target_item = target_path / item.name
                if not target_item.exists() or self._is_conflict(item, target_item):
                    self._resolve_conflict(item, target_item)
                else:
                    self._copy_file(item, target_item)
        
        self._update_index(target_path)

    def _is_conflict(self, source_file, target_file):
        return source_file.stat().st_mtime != target_file.stat().st_mtime

    def _resolve_conflict(self, source_file, target_file):
        choice = input(f"Conflict detected for {source_file.name}. Keep 's'ource or 't'arget? ")
        if choice.lower() == 's':
            self._copy_file(source_file, target_file)
        elif choice.lower() == 't':
            pass  # Keep the target file as it is
        else:
            print("Invalid choice. Skipping conflict resolution.")

    def _copy_file(self, source_file, target_file):
        with open(source_file, 'rb') as src, open(target_file, 'wb') as tgt:
            tgt.write(src.read())
        print(f"Copied {source_file} to {target_file}")

    def _update_index(self, directory):
        index_file = directory / 'index.txt'
        with open(index_file, 'w') as idx:
            for item in directory.iterdir():
                if item.is_file() and item.suffix == '.md':
                    idx.write(f"{item.name}\n")
        print(f"Index updated at {index_file}")