package api

import (
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/axentx/surrogate-1/backend/models"
)

// Evidence stores training artifact and policy evaluation metadata
type Evidence struct {
	RunID         string    `json:"run_id"`
	Timestamp     time.Time `json:"timestamp"`
	PolicyVersion string    `json:"policy_version"`
	ModelSHA      string    `json:"model_sha"`
	ArtifactURL   string    `json:"artifact_url"`
}

// EvidenceResponse wraps the evidence list with pagination
type EvidenceResponse struct {
	Evidence []Evidence `json:"evidence"`
	Total    int        `json:"total"`
}

// EvidenceHandler handles /api/evidence requests
type EvidenceHandler struct {
	s3Client *s3.Client
}

// NewEvidenceHandler creates a new EvidenceHandler
func NewEvidenceHandler() *EvidenceHandler {
	cfg, err := config.LoadDefaultConfig(aws.Config{})
	if err != nil {
		panic(fmt.Sprintf("failed to load AWS config: %v", err))
	}

	s3Client := s3.NewFromConfig(cfg)

	return &EvidenceHandler{
		s3Client: s3Client,
	}
}

// GetEvidence retrieves evidence records filtered by run_id
func (h *EvidenceHandler) GetEvidence(w http.ResponseWriter, r *http.Request) {
	runID := r.URL.Query().Get("run_id")

	var evidence []Evidence
	var total int

	if runID != "" {
		evidence, total = h.getEvidenceByRunID(runID)
	} else {
		evidence, total = h.getAllEvidence()
	}

	response := EvidenceResponse{
		Evidence: evidence,
		Total:    total,
	}

	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("X-Response-Time", fmt.Sprintf("%dms", time.Since(r.Time).Milliseconds()))

	if err := json.NewEncoder(w).Encode(response); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
}

// getEvidenceByRunID retrieves evidence for a specific run
func (h *EvidenceHandler) getEvidenceByRunID(runID string) ([]Evidence, int) {
	// In production, this would query a database or S3 metadata store
	// For now, we simulate with in-memory lookup
	evidence := []Evidence{}
	total := 0

	// Simulate evidence retrieval - in real implementation, query from database
	// This would check S3 for artifacts matching the run_id
	// and return metadata including model SHA, policy version, etc.

	return evidence, total
}

// getAllEvidence retrieves all evidence records
func (h *EvidenceHandler) getAllEvidence() ([]Evidence, int) {
	evidence := []Evidence{}
	total := 0

	// In production, this would query a database or S3 metadata store
	return evidence, total
}

// UploadEvidenceToS3 uploads evidence artifacts to S3
func (h *EvidenceHandler) UploadEvidenceToS3(runID string, modelPath string, policyVersion string) error {
	cfg, err := config.LoadDefaultConfig(aws.Config{})
	if err != nil {
		return fmt.Errorf("failed to load AWS config: %w", err)
	}

	s3Client := s3.NewFromConfig(cfg)

	// Upload model artifact
	modelKey := fmt.Sprintf("artifacts/%s/model.bin", runID)
	modelFile, err := os.Open(modelPath)
	if err != nil {
		return fmt.Errorf("failed to open model file: %w", err)
	}
	defer modelFile.Close()

	_, err = s3Client.PutObject(&s3.PutObjectInput{
		Bucket: aws.String(os.Getenv("S3_BUCKET")),
		Key:    aws.String(modelKey),
		Body:   modelFile,
	})
	if err != nil {
		return fmt.Errorf("failed to upload model to S3: %w", err)
	}

	// Upload training logs
	logsKey := fmt.Sprintf("artifacts/%s/training_logs.json", runID)
	logsFile, err := os.Open(fmt.Sprintf("%s/training_logs.json", modelPath))
	if err == nil {
		defer logsFile.Close()
		_, err = s3Client.PutObject(&s3.PutObjectInput{
			Bucket: aws.String(os.Getenv("S3_BUCKET")),
			Key:    aws.String(logsKey),
			Body:   logsFile,
		})
		if err != nil {
			return fmt.Errorf("failed to upload logs to S3: %w", err)
		}
	}

	// Upload policy evaluation results
	policyKey := fmt.Sprintf("artifacts/%s/policy_evaluation.json", runID)
	policyFile, err := os.Open(fmt.Sprintf("%s/policy_evaluation.json", modelPath))
	if err == nil {
		defer policyFile.Close()
		_, err = s3Client.PutObject(&s3.PutObjectInput{
			Bucket: aws.String(os.Getenv("S3_BUCKET")),
			Key:    aws.String(policyKey),
			Body:   policyFile,
		})
		if err != nil {
			return fmt.Errorf("failed to upload policy evaluation to S3: %w", err)
		}
	}

	return nil
}

// CalculateModelSHA computes SHA256 hash of model artifact
func CalculateModelSHA(modelPath string) (string, error) {
	data, err := os.ReadFile(modelPath)
	if err != nil {
		return "", err
	}

	// Compute SHA256
	hash := fmt.Sprintf("%x", sha256.Sum256(data))
	return hash, nil
}