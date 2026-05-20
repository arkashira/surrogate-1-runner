import * as path from "path";

/**
 * Detects the programming language based on a file's extension.
 *
 * Returns a lower‑cased language identifier that can be used by downstream
 * components (e.g. for syntax highlighting or model prompting). If the
 * extension is unknown, `"plaintext"` is returned.
 *
 * @param filePath Full path (or just the filename) of the file to inspect.
 */
export function detectLanguage(filePath: string): string {
  const ext = path.extname(filePath).toLowerCase();

  const extensionMap: Record<string, string> = {
    ".js": "javascript",
    ".mjs": "javascript",
    ".cjs": "javascript",
    ".ts": "typescript",
    ".tsx": "typescript",
    ".jsx": "javascript",
    ".py": "python",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".cs": "csharp",
    ".rb": "ruby",
    ".go": "go",
    ".rs": "rust",
    ".php": "php",
    ".html": "html",
    ".htm": "html",
    ".css": "css",
    ".scss": "scss",
    ".json": "json",
    ".md": "markdown",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".sh": "shell",
    ".bash": "shell",
    ".zsh": "shell",
    ".tsx": "typescript",
    ".vue": "vue",
    ".swift": "swift",
    ".kt": "kotlin",
    ".kts": "kotlin",
    ".dart": "dart",
    ".scala": "scala",
    ".pl": "perl",
    ".r": "r",
    ".sql": "sql",
    ".tsx": "typescript",
  };

  return extensionMap[ext] ?? "plaintext";
}