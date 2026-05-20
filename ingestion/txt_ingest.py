import os
from pathlib import Path

def ingest_txt(file_path, output_dir):
    """
    Ingests a TXT file and stores it in the specified output directory.
    
    :param file_path: Path to the TXT file to be ingested.
    :param output_dir: Directory where the ingested document will be stored.
    """
    # Ensure the output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    try:
        # Read the content of the TXT file
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Define the output file path
        output_file_path = os.path.join(output_dir, os.path.basename(file_path))
        
        # Write the content to the output directory
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(content)
        
        print(f"Successfully ingested {file_path} and stored in {output_dir}")
    except Exception as e:
        print(f"Error ingesting {file_path}: {str(e)}")

# Example usage
if __name__ == "__main__":
    txt_file_path = "/path/to/sample.txt"
    output_directory = "/path/to/output"
    ingest_txt(txt_file_path, output_directory)