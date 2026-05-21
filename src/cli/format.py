#!/usr/bin/env python3
"""
surrogate format - Format codebase in a repository.

Usage:
    surrogate format --repo <path> [--lang <language>]
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        prog="surrogate format",
        description="Format all supported files in a repository.",
    )
    parser.add_argument(
        "--repo",
        type=str,
        required=True,
        help="Path to the repository to format",
    )
    parser.add_argument(
        "--lang",
        type=str,
        default=None,
        help="Language to format (optional, formats all if not specified)",
    )
    return parser.parse_args()


def get_supported_extensions(lang: Optional[str]) -> List[str]:
    """Get file extensions based on language filter."""
    lang_map = {
        "python": [".py"],
        "javascript": [".js", ".jsx", ".mjs"],
        "typescript": [".ts", ".tsx"],
        "go": [".go"],
        "rust": [".rs"],
        "java": [".java"],
        "c": [".c", ".h"],
        "cpp": [".cpp", ".hpp", ".cc", ".cxx", ".hxx"],
        "csharp": [".cs"],
        "ruby": [".rb"],
        "php": [".php"],
        "swift": [".swift"],
        "kotlin": [".kt", ".kts"],
        "scala": [".scala"],
        "html": [".html", ".htm"],
        "css": [".css", ".scss", ".sass"],
        "json": [".json"],
        "yaml": [".yaml", ".yml"],
        "xml": [".xml"],
        "markdown": [".md"],
        "sql": [".sql"],
    }
    
    if lang is None:
        return sorted(lang_map.keys())
    
    return lang_map.get(lang, [])


def format_file(filepath: Path) -> bool:
    """Format a single file. Returns True if formatted, False if skipped."""
    try:
        # Check if file is readable
        if not filepath.is_file():
            return False
        
        # Check extension
        ext = filepath.suffix.lower()
        if ext not in get_supported_extensions(None):
            return False
        
        # Read file
        content = filepath.read_text(encoding="utf-8")
        
        # Format based on language (placeholder - actual formatter would go here)
        # For now, we just validate the file exists and is readable
        if not content:
            return False
        
        # Write back (in real implementation, would use actual formatter)
        filepath.write_text(content, encoding="utf-8")
        
        return True
    except Exception:
        return False


def format_repo(repo_path: str, lang: Optional[str]) -> int:
    """Format all files in a repository. Returns exit code."""
    repo = Path(repo_path)
    
    if not repo.exists():
        print(f"Error: Repository path does not exist: {repo_path}", file=sys.stderr)
        return 1
    
    if not repo.is_dir():
        print(f"Error: Path is not a directory: {repo_path}", file=sys.stderr)
        return 1
    
    supported_langs = get_supported_extensions(lang)
    formatted_count = 0
    error_count = 0
    
    print(f"Formatting repository: {repo_path}")
    print(f"Supported languages: {', '.join(supported_langs)}")
    print()
    
    # Find all files
    for filepath in repo.rglob("*"):
        if filepath.is_file():
            ext = filepath.suffix.lower()
            if ext in supported_langs:
                if format_file(filepath):
                    formatted_count += 1
                else:
                    error_count += 1
    
    # Print summary
    print()
    print("Summary:")
    print(f"  Files formatted: {formatted_count}")
    print(f"  Files skipped: {error_count}")
    
    if error_count > 0:
        return 1
    
    return 0


def main() -> int:
    """Main entry point."""
    args = parse_args()
    return format_repo(args.repo, args.lang)


if __name__ == "__main__":
    sys.exit(main())