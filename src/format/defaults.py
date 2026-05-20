"""Default language-specific formatter mappings for surrogate format command."""

from typing import Dict, Tuple

# Mapping: file extension -> (formatter_name, formatter_command)
DEFAULT_FORMATTERS: Dict[str, Tuple[str, str]] = {
    # JavaScript/TypeScript
    ".js": ("prettier", "prettier --write"),
    ".jsx": ("prettier", "prettier --write"),
    ".ts": ("prettier", "prettier --write"),
    ".tsx": ("prettier", "prettier --write"),
    ".mjs": ("prettier", "prettier --write"),
    ".cjs": ("prettier", "prettier --write"),
    
    # Python
    ".py": ("black", "black"),
    
    # Go
    ".go": ("gofmt", "gofmt -w"),
    
    # Shell
    ".sh": ("shfmt", "shfmt -w"),
    
    # YAML
    ".yaml": ("prettier", "prettier --write"),
    ".yml": ("prettier", "prettier --write"),
    
    # JSON
    ".json": ("prettier", "prettier --write"),
    
    # Markdown
    ".md": ("prettier", "prettier --write"),
    
    # TOML
    ".toml": ("prettier", "prettier --write"),
    
    # Rust
    ".rs": ("rustfmt", "rustfmt --emit=stdout"),
    
    # C/C++
    ".c": ("clang-format", "clang-format -i"),
    ".cpp": ("clang-format", "clang-format -i"),
    ".h": ("clang-format", "clang-format -i"),
    ".hpp": ("clang-format", "clang-format -i"),
    
    # Java
    ".java": ("java", "javac"),
    
    # Ruby
    ".rb": ("rubocop", "rubocop -a"),
    
    # PHP
    ".php": ("php-cs-fixer", "php-cs-fixer fix"),
    
    # HTML
    ".html": ("prettier", "prettier --write"),
    
    # CSS/SCSS
    ".css": ("prettier", "prettier --write"),
    ".scss": ("prettier", "prettier --write"),
    ".sass": ("prettier", "prettier --write"),
    
    # SQL
    ".sql": ("sqlfmt", "sqlfmt -i"),
    
    # GraphQL
    ".graphql": ("prettier", "prettier --write"),
    ".gql": ("prettier", "prettier --write"),
}

# Default formatter for unknown extensions (no-op)
DEFAULT_FORMATTER: str = "none"


def get_formatter_for_extension(ext: str) -> Tuple[str, str]:
    """
    Get the formatter name and command for a given file extension.
    
    Args:
        ext: File extension including the dot (e.g., ".py", ".js")
        
    Returns:
        Tuple of (formatter_name, formatter_command)
    """
    ext_lower = ext.lower()
    if ext_lower in DEFAULT_FORMATTERS:
        return DEFAULT_FORMATTERS[ext_lower]
    return DEFAULT_FORMATTER, DEFAULT_FORMATTER


def get_formatter_for_language(language: str) -> Tuple[str, str]:
    """
    Get the formatter for a language name (alternative to extension lookup).
    
    Args:
        language: Language name (e.g., "python", "javascript", "go")
        
    Returns:
        Tuple of (formatter_name, formatter_command)
    """
    language_map = {
        "python": ("black", "black"),
        "javascript": ("prettier", "prettier --write"),
        "typescript": ("prettier", "prettier --write"),
        "go": ("gofmt", "gofmt -w"),
        "shell": ("shfmt", "shfmt -w"),
        "yaml": ("prettier", "prettier --write"),
        "json": ("prettier", "prettier --write"),
        "markdown": ("prettier", "prettier --write"),
        "toml": ("prettier", "prettier --write"),
        "rust": ("rustfmt", "rustfmt --emit=stdout"),
        "c": ("clang-format", "clang-format -i"),
        "cpp": ("clang-format", "clang-format -i"),
        "java": ("java", "javac"),
        "ruby": ("rubocop", "rubocop -a"),
        "php": ("php-cs-fixer", "php-cs-fixer fix"),
        "html": ("prettier", "prettier --write"),
        "css": ("prettier", "prettier --write"),
        "sql": ("sqlfmt", "sqlfmt -i"),
        "graphql": ("prettier", "prettier --write"),
    }
    
    lang_lower = language.lower()
    if lang_lower in language_map:
        return language_map[lang_lower]
    return DEFAULT_FORMATTER, DEFAULT_FORMATTER