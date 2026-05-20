import argparse
import sys
from .validate import validate_command

def main():
    parser = argparse.ArgumentParser(description='Surrogate-1 CLI')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Run validation on a YAML file')
    validate_parser.add_argument('yaml_file', help='Path to validation YAML file')

    args = parser.parse_args()

    if args.command == 'validate':
        validate_command(args.yaml_file)
    elif args.command is None:
        parser.print_help()
        sys.exit(1)

if __name__ == '__main__':
    main()