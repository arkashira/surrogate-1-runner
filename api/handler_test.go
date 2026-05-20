package api

import (
	"archive/zip"
	"bytes"
	"io"
	"mime/multipart"
	"net/http"
	"net/http/httptest"
	"path/filepath"
	"testing"
)

/*
   Helper: build a multipart/form‑data request that carries a single file.
   The function returns a *http.Request ready to be handed to the handler.
*/
func newFileUploadRequest(uri, paramName, fileName string, fileContent []byte) (*http.Request, error) {
	body := &bytes.Buffer{}
	w := multipart.NewWriter(body)

	part, err := w.CreateFormFile(paramName, filepath.Base(fileName))
	if err != nil {
		return nil, err
	}
	if _, err = part.Write(fileContent); err != nil {
		return nil, err
	}
	if err = w.Close(); err != nil {
		return nil, err
	}

	req, err := http.NewRequest(http.MethodPost, uri, body)
	if err != nil {
		return nil, err
	}
	req.Header.Set("Content-Type", w.FormDataContentType())
	return req, nil
}

/*
   Integration test for the /mesh endpoint.
   Expected contract (as inferred from the original task):
   • POST /mesh with a file → 200 OK
   • Response body is a ZIP archive (Content‑Type: application/zip)
   • The ZIP contains at least one file; if the input was an OBJ we expect the same OBJ inside.
*/
func TestMeshHandlerIntegration(t *testing.T) {
	// 1️⃣  Small, valid OBJ payload – enough to prove the round‑trip works.
	const dummyOBJ = "v 0.0 0.0 0.0\nv 1.0 0.0 0.0\nv 0.0 1.0 0.0\nf 1 2 3\n"
	req, err := newFileUploadRequest("/mesh", "file", "dummy.obj", []byte(dummyOBJ))
	if err != nil {
		t.Fatalf("building request failed: %v", err)
	}

	// 2️⃣  Record the handler’s response.
	rr := httptest.NewRecorder()
	// MeshHandler must be exported from the api package (or replace with the actual handler name).
	handler := http.HandlerFunc(MeshHandler)
	handler.ServeHTTP(rr, req)

	// 3️⃣  Basic HTTP contract checks.
	if got, want := rr.Code, http.StatusOK; got != want {
		t.Fatalf("unexpected status: got %d, want %d", got, want)
	}
	if ct := rr.Header().Get("Content-Type"); ct != "application/zip" {
		t.Fatalf("unexpected Content‑Type: got %s, want application/zip", ct)
	}

	// 4️⃣  Parse the response body as a ZIP archive.
	zr, err := zip.NewReader(bytes.NewReader(rr.Body.Bytes()), int64(rr.Body.Len()))
	if err != nil {
		t.Fatalf("response is not a valid zip archive: %v", err)
	}
	if len(zr.File) == 0 {
		t.Fatalf("zip archive is empty")
	}

	// 5️⃣  Verify that the archive contains the original OBJ (or at least one .obj file).
	found := false
	for _, f := range zr.File {
		if filepath.Ext(f.Name) != ".obj" {
			continue
		}
		found = true
		rc, err := f.Open()
		if err != nil {
			t.Fatalf("cannot open %s inside zip: %v", f.Name, err)
		}
		content, err := io.ReadAll(rc)
		rc.Close()
		if err != nil {
			t.Fatalf("cannot read %s inside zip: %v", f.Name, err)
		}
		if !bytes.Equal(content, []byte(dummyOBJ)) {
			t.Fatalf("content mismatch for %s", f.Name)
		}
		break
	}
	if !found {
		t.Fatalf("expected at least one .obj file inside the zip archive")
	}
}

/*
   Benchmark – measures how the handler behaves with a larger payload.
   The SLA mentioned in the original brief is “process a 1 GB file in <30 s”.
   Running a full‑scale 1 GB payload in CI is impractical, so we benchmark with a
   10 MiB payload that still stresses the code path (multipart parsing, streaming,
   zip creation).  The benchmark can be scaled up locally if needed.
*/
func BenchmarkMeshHandler_10MiB(b *testing.B) {
	const payloadSize = 10 * 1024 * 1024 // 10 MiB
	// Fill the buffer with deterministic data – easier on the GC than random bytes.
	payload := make([]byte, payloadSize)
	for i := range payload {
		payload[i] = byte(i % 256)
	}

	req, err := newFileUploadRequest("/mesh", "file", "large.bin", payload)
	if err != nil {
		b.Fatalf("building request failed: %v", err)
	}
	handler := http.HandlerFunc(MeshHandler)

	b.ResetTimer()
	for i := 0; i < b.N; i++ {
		rr := httptest.NewRecorder()
		handler.ServeHTTP(rr, req)

		if rr.Code != http.StatusOK {
			b.Fatalf("unexpected status %d", rr.Code)
		}
		// No need to read the body – we only care about processing time.
	}
}