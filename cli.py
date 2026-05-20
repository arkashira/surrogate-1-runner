#!/usr/bin/env python3

import argparse
import json
import sys
from typing import Dict, Any

from surrogate1.reporter import Reporter

def main():
    parser = argparse.ArgumentParser(description='Run surrogate-1 checks.')
    parser.add_argument('--output', help='Output file path for JSON results')
    args = parser.parse_args()

    reporter = Reporter()

    try:
        reporter.run_checks()
        result = {
            'pass': True,
            'details': reporter.details,
            'summary': reporter.summary
        }
        print(json.dumps(result))

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f)

        sys.exit(0)
    except Exception as e:
        result = {
            'pass': False,
            'details': reporter.details,
            'summary': str(e)
        }
        print(json.dumps(result))

        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f)

        sys.exit(1)

if __name__ == '__main__':
    main()