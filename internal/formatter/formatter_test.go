package formatter

import (
	"bytes"
	"io"
	"log"
	"testing"
)

func TestDefaultMappingExists(t *testing.T) {
	f := NewFormatter(log.New(io.Discard, "", 0))

	tests := []struct {
		ext string
		cmd string
	}{
		{".go", "gofmt"},
		{".py", "black"},
		{".js", "prettier"},
		{".ts", "prettier"},
		{".json", "prettier"},
		{".css", "prettier"},
		{".html", "prettier"},
	}

	for _, tt := range tests {
		args, ok := f.extMap[tt.ext]
		if !ok {
			t.Fatalf("extension %s not found in mapping", tt.ext)
		}
		if args[0] != tt.cmd {
			t.Fatalf("expected command %s for %s, got %s", tt.cmd, tt.ext, args[0])
		}
	}
}

func TestUnsupportedExtensionProducesWarning(t *testing.T) {
	var buf bytes.Buffer
	logger := log.New(&buf, "", 0)
	f := NewFormatter(logger)

	err := f.FormatFile("example.unknown")
	if err != nil {
		t.Fatalf("expected nil error for unsupported file, got %v", err)
	}
	if !bytes.Contains(buf.Bytes(), []byte("warning: no formatter configured")) {
		t.Fatalf("expected warning log, got %q", buf.String())
	}
}