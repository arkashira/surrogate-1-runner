package evidence

import (
	"context"
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"sync"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/service/s3"
)

// S3Uploader abstracts the subset of the S3 client we need for uploading.
type S3Uploader interface {
	PutObject(ctx context.Context, params *s3.PutObjectInput, optFns ...func(*s3.Options)) (*s3.PutObjectOutput, error)
}

// Metadata holds the persisted information for a single pipeline run.
type Metadata struct {
	RunID         string `json:"run_id"`
	Timestamp     string `json:"timestamp"` // RFC3339
	PolicyVersion string `json:"policy_version"`
	ModelSHA256   string `json:"model_sha256"`
	ModelURL      string `json:"model_url"`
	LogsURL       string `json:"logs_url"`
	PolicyURL     string `json:"policy_url"`
}

// EvidenceCollector handles artifact uploads and metadata persistence.
type EvidenceCollector struct {
	s3Client S3Uploader
	bucket   string

	// simple in‑memory store; in production this would be a DB.
	mu       sync.RWMutex
	metadata map[string]Metadata
}

// NewEvidenceCollector creates a new collector instance.
func NewEvidenceCollector(s3Client S3Uploader, bucket string) *EvidenceCollector {
	return &EvidenceCollector{
		s3Client: s3Client,
		bucket:   bucket,
		metadata: make(map[string]Metadata),
	}
}

// Collect uploads the supplied artifacts and records their metadata.
func (c *EvidenceCollector) Collect(ctx context.Context, runID string, modelPath string, logsPath string, policyJSONPath string, policyVersion string) error {
	ts := time.Now().UTC().Format(time.RFC3339)

	// Upload model binary and compute SHA256.
	modelSHA, err := computeSHA256(modelPath)
	if err != nil {
		return err
	}
	modelKey := filepath.Join(runID, "model", filepath.Base(modelPath))
	modelURL, err := c.uploadFile(ctx, modelPath, modelKey)
	if err != nil {
		return err
	}

	// Upload training logs.
	logsKey := filepath.Join(runID, "logs", filepath.Base(logsPath))
	logsURL, err := c.uploadFile(ctx, logsPath, logsKey)
	if err != nil {
		return err
	}

	// Upload policy evaluation JSON.
	policyKey := filepath.Join(runID, "policy", filepath.Base(policyJSONPath))
	policyURL, err := c.uploadFile(ctx, policyJSONPath, policyKey)
	if err != nil {
		return err
	}

	// Persist metadata.
	meta := Metadata{
		RunID:         runID,
		Timestamp:     ts,
		PolicyVersion: policyVersion,
		ModelSHA256:   modelSHA,
		ModelURL:      modelURL,
		LogsURL:       logsURL,
		PolicyURL:     policyURL,
	}
	c.mu.Lock()
	c.metadata[runID] = meta
	c.mu.Unlock()
	return nil
}

// uploadFile streams a local file to S3 and returns the public URL.
func (c *EvidenceCollector) uploadFile(ctx context.Context, localPath string, s3Key string) (string, error) {
	f, err := os.Open(localPath)
	if err != nil {
		return "", err
	}
	defer f.Close()

	_, err = c.s3Client.PutObject(ctx, &s3.PutObjectInput{
		Bucket: aws.String(c.bucket),
		Key:    aws.String(s3Key),
		Body:   f,
	})
	if err != nil {
		return "", err
	}
	// Construct a simple S3 URL (assuming bucket is public or presigned elsewhere).
	url := "https://" + c.bucket + ".s3.amazonaws.com/" + s3Key
	return url, nil
}

// computeSHA256 returns the hex‑encoded SHA256 of the file at path.
func computeSHA256(path string) (string, error) {
	f, err := os.Open(path)
	if err != nil {
		return "", err
	}
	defer f.Close()
	h := sha256.New()
	if _, err := io.Copy(h, f); err != nil {
		return "", err
	}
	return hex.EncodeToString(h.Sum(nil)), nil
}

// GetEvidenceHandler returns a JSON payload for a given run_id query param.
func (c *EvidenceCollector) GetEvidenceHandler(w http.ResponseWriter, r *http.Request) {
	runID := r.URL.Query().Get("run_id")
	if runID == "" {
		http.Error(w, "`run_id` query parameter required", http.StatusBadRequest)
		return
	}

	c.mu.RLock()
	meta, ok := c.metadata[runID]
	c.mu.RUnlock()
	if !ok {
		http.Error(w, "evidence not found", http.StatusNotFound)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	enc := json.NewEncoder(w)
	enc.SetEscapeHTML(false)
	_ = enc.Encode(meta)
}