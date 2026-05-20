package formatter

import (
	"os/exec"
	"path/filepath"
	"strings"
)

type Formatter struct {
	commands map[string]string
}

func NewFormatter() *Formatter {
	return &Formatter{
		commands: map[string]string{
			".go":  "gofmt",
			".py": "black",
			".js": "prettier",
		},
	}
}

func (f *Formatter) Format(filePath string) error {
	ext := filepath.Ext(filePath)
	formatter, ok := f.commands[ext]
	if !ok {
		return fmt.Errorf("unsupported file type: %s", ext)
	}

	cmd := exec.Command(formatter, filePath)
	err := cmd.Run()
	if err != nil {
		return fmt.Errorf("formatter error: %v", err)
	}

	return nil
}