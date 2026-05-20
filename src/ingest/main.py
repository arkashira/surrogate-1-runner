import os
from docx_ingestor import DocxIngestor

def main():
    input_dir = "/path/to/input/directory"
    output_dir = "/path/to/output/directory"

    docx_ingestor = DocxIngestor(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".docx"):
            file_path = os.path.join(input_dir, filename)
            docx_ingestor.ingest(file_path)

if __name__ == "__main__":
    main()