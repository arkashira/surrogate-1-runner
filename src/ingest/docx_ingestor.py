import os
import docx
from typing import List

class DocxIngestor:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)

    def ingest(self, file_path: str) -> str:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        output_path = os.path.join(self.output_dir, os.path.basename(file_path) + ".txt")
        with open(output_path, "w") as f:
            f.write(text)
        return output_path