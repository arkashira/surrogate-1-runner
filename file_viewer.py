import os
import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MarkdownFileHandler(FileSystemEventHandler):
    def __init__(self, link_graph):
        self.link_graph = link_graph

    def on_modified(self, event):
        if not event.is_directory:
            self.link_graph.update(event.src_path)

def watch_files(link_graph, path):
    event_handler = MarkdownFileHandler(link_graph)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

# /opt/axentx/surrogate-1/link_graph.py
import networkx as nx
import os

class LinkGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def update(self, file_path):
        # Update graph logic here based on the content of the file_path
        pass

    def display(self):
        # Display graph logic here
        pass

# /opt/axentx/surrogate-1/main.py
import sys
sys.path.append('/opt/axentx/surrogate-1')

from file_viewer import watch_files
from link_graph import LinkGraph

def main():
    link_graph = LinkGraph()
    watch_files(link_graph, '/path/to/markdown/files')

if __name__ == '__main__':
    main()

## Summary
- Added `MarkdownFileHandler` to watch for changes in markdown files
- Updated `LinkGraph` class to include `update` method for real-time updates
- Modified `main` function to integrate link-graph visualization with file viewer
- Real-time updates and display of link-graph are not implemented yet, as the logic depends on the specific metadata and relationship between files