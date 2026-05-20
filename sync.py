import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .encryption import FileEncryptor

class SyncHandler(FileSystemEventHandler):
    def __init__(self):
        self.encryptor = FileEncryptor()

    def on_modified(self, event):
        if event.is_directory:
            return
        print(f'File {event.src_path} has been modified.')
        self.encryptor.encrypt_file(event.src_path)

def start_sync_watch(path):
    event_handler = SyncHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(60 * 5)  # Check every 5 minutes
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

if __name__ == "__main__":
    directory_to_watch = '/path/to/markdown/files'
    start_sync_watch(directory_to_watch)