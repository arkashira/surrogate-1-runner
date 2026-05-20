package services

import (
	"bytes"
	"context"
	"encoding/base64"
	"fmt"
	"html"
	"io"
	"mime"
	"net/http"
	"os"
	"path/filepath"
)

// ---------------------------------------------------------------------
// 1️⃣  FilePreviewService – HTTP handler
// ---------------------------------------------------------------------

// FilePreviewService streams files from a base directory.
// The handler is safe against directory traversal and automatically
// detects the MIME type of the requested file.
type FilePreviewService struct {
	baseDir string
}

// NewFilePreviewService creates a new service instance.
func NewFilePreviewService(baseDir string) *FilePreviewService {
	return &FilePreviewService{baseDir: baseDir}
}

// Handler returns an http.Handler that serves file previews.
// URL pattern: /preview/<relative-path>
func (s *FilePreviewService) Handler() http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// 1️⃣  Strip the prefix
		const prefix = "/preview/"
		if !filepath.HasPrefix(r.URL.Path, prefix) {
			http.Error(w, "invalid endpoint", http.StatusNotFound)
			return
		}
		relPath := r.URL.Path[len(prefix):]
		if relPath == "" {
			http.Error(w, "file not specified", http.StatusBadRequest)
			return
		}

		// 2️⃣  Prevent directory traversal
		cleanPath := filepath.Clean(relPath)
		if cleanPath != relPath || cleanPath == ".." || cleanPath == "." {
			http.Error(w, "invalid file path", http.StatusBadRequest)
			return
		}

		fullPath := filepath.Join(s.baseDir, cleanPath)

		f, err := os.Open(fullPath)
		if err != nil {
			if os.IsNotExist(err) {
				http.Error(w, "file not found", http.StatusNotFound)
			} else {
				http.Error(w, "internal error", http.StatusInternalServerError)
			}
			return
		}
		defer f.Close()

		// 3️⃣  Detect MIME type
		mimeType := mime.TypeByExtension(filepath.Ext(fullPath))
		if mimeType == "" {
			// Fallback: sniff first 512 bytes
			var buf [512]byte
			n, _ := f.Read(buf[:])
			mimeType = http.DetectContentType(buf[:n])
			// rewind
			f.Seek(0, io.SeekStart)
		}

		// 4️⃣  Set headers and stream
		w.Header().Set("Content-Type", mimeType)
		w.Header().Set("Content-Disposition", fmt.Sprintf(`inline; filename="%s"`, filepath.Base(fullPath)))
		w.WriteHeader(http.StatusOK)

		if _, err := io.Copy(w, f); err != nil {
			// Client disconnected – ignore
			return
		}
	})
}

// ServePreview starts a simple HTTP server that serves previews from
// baseDir.  It is meant for local testing or quick demos.
func ServePreview(ctx context.Context, addr, baseDir string) error {
	srv := &http.Server{
		Addr:    addr,
		Handler: NewFilePreviewService(baseDir).Handler(),
	}
	go func() {
		<-ctx.Done()
		srv.Shutdown(context.Background())
	}()
	return srv.ListenAndServe()
}

// ---------------------------------------------------------------------
// 2️⃣  RenderPreview – HTML snippet for inline preview
// ---------------------------------------------------------------------

// RenderPreview turns raw file data into an HTML snippet that can be
// embedded directly into a page.
//
// Supported MIME types:
//   * application/pdf
//   * image/*
//   * text/*
// Unsupported types are rendered as a download link.
func RenderPreview(mimeType string, data []byte) (string, error) {
	switch {
	case mimeType == "application/pdf":
		encoded := base64.StdEncoding.EncodeToString(data)
		return fmt.Sprintf(`
<div style="width:100%%;height:80vh;">
  <embed src="data:application/pdf;base64,%s" type="application/pdf"
         width="100%%" height="100%%" />
</div>`, encoded), nil

	case mime.HasPrefix(mimeType, "image/"):
		encoded := base64.StdEncoding.EncodeToString(data)
		return fmt.Sprintf(`
<div style="text-align:center;">
  <img src="data:%s;base64,%s" alt="Image preview"
       style="max-width:100%%;height:auto;" />
</div>`, mimeType, encoded), nil

	case mime.HasPrefix(mimeType, "text/"):
		escaped := html.EscapeString(string(data))
		return fmt.Sprintf(`
<div style="overflow:auto;">
  <pre style="background:#f8f8f8;padding:1rem;border:1px solid #ddd;">%s</pre>
</div>`, escaped), nil

	default:
		// Fallback: download link
		encoded := base64.StdEncoding.EncodeToString(data)
		filename := "download"
		return fmt.Sprintf(`
<div style="text-align:center;">
  <a href="data:%s;base64,%s" download="%s">Download %s</a>
</div>`, mimeType, encoded, filename, filename), nil
	}
}