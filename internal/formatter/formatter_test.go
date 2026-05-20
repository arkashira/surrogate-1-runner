package formatter

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestFormatter_Format(t *testing.T) {
	f := NewFormatter()

	testCases := []struct {
		name     string
		filePath string
		wantErr  bool
	}{
		{"go", "testdata/go/main.go", false},
		{"py", "testdata/python/main.py", false},
		{"js", "testdata/js/main.js", false},
		{"unknown", "testdata/unknown/file.txt", true},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			err := f.Format(tc.filePath)
			if tc.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}