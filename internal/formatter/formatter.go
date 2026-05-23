package formatter

import (
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
)

// Formatter maps file extensions to their corresponding formatter commands and arguments
type Formatter struct {
	extension string
	command   string
	args      []string
}

// Formatters defines the mapping of file extensions to formatter commands and arguments
var Formatters = map[string]Formatter{
	".go": {
		extension: ".go",
		command:   "gofmt",
		args:      []string{"-w", "-s"},
	},
	".py": {
		extension: ".py",
		command:   "black",
		args:      []string{"--line-length", "88"},
	},
	".js": {
		extension: ".js",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".ts": {
		extension: ".ts",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".jsx": {
		extension: ".jsx",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".tsx": {
		extension: ".tsx",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".json": {
		extension: ".json",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".yaml": {
		extension: ".yaml",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".yml": {
		extension: ".yml",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".md": {
		extension: ".md",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".html": {
		extension: ".html",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".css": {
		extension: ".css",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".scss": {
		extension: ".scss",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".less": {
		extension: ".less",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".graphql": {
		extension: ".graphql",
		command:   "prettier",
		args:      []string{"--write"},
	},
	".sql": {
		extension: ".sql",
		command:   "prettier",
		args:      []string{"--write"},
	},
}

// GetFormatter returns the formatter for a given file path
func GetFormatter(filePath string) (*Formatter, error) {
	ext := filepath.Ext(filePath)
	if formatter, ok := Formatters[ext]; ok {
		return &formatter, nil
	}
	return nil, fmt.Errorf("unsupported file extension: %s", ext)
}

// FormatFile formats a single file using the appropriate formatter
func FormatFile(filePath string) error {
	formatter, err := GetFormatter(filePath)
	if err != nil {
		fmt.Fprintf(os.Stderr, "WARNING: Skipping unsupported file: %s\n", filePath)
		return nil
	}

	cmd := exec.Command(formatter.command, append(formatter.args, filePath)...)
	cmd.Stdin = nil
	cmd.Stdout = os.Stdout
	cmd.Stderr = os.Stderr

	if err := cmd.Run(); err != nil {
		return fmt.Errorf("formatter error for %s: %w", filePath, err)
	}

	fmt.Printf("Formatted file %s successfully\n", filePath)
	return nil
}

// FormatDirectory formats all supported files in a directory recursively
func FormatDirectory(dirPath string) error {
	err := filepath.Walk(dirPath, func(path string, info os.FileInfo, err error) error {
		if err != nil {
			return err
		}

		if !info.IsDir() {
			return FormatFile(path)
		}
		return nil
	})

	return err
}

// FormatFiles formats multiple files at once
func FormatFiles(filePaths []string) error {
	var errors []error
	for _, filePath := range filePaths {
		if err := FormatFile(filePath); err != nil {
			errors = append(errors, err)
		}
	}

	if len(errors) > 0 {
		return fmt.Errorf("formatter errors: %v", errors)
	}
	return nil
}