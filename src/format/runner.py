import argparse
import subprocess

def format_files(config_file=None):
    parser = argparse.ArgumentParser(description='Format files using language-specific defaults.')
    parser.add_argument('--config', help='Path to custom config file', default=config_file)
    args = parser.parse_args()

    # Map file extensions to formatters
    formatters = {
        '.js': 'prettier',
        '.ts': 'prettier',
        '.py': 'black',
        '.go': 'gofmt',
    }

    # Get all files in the repository
    files = subprocess.check_output(['git', 'ls-files']).decode().split('\n')

    for file in files:
        ext = file.split('.')[-1]
        if ext in formatters:
            formatter = formatters[ext]
            subprocess.run(['surrogate', 'format', file, '--formatter', formatter, '--config', args.config], check=True)
            print(f"Formatted {file} with {formatter}")

if __name__ == "__main__":
    format_files()