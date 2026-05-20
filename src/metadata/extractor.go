package metadata

import (
	"database/sql"
	"encoding/json"
	"fmt"

	_ "github.com/lib/pq"
)

type ModelArtifact struct {
	DatasetSource string                 `json:"dataset_source"`
	BiasMetrics   map[string]interface{} `json:"bias_metrics"`
}

func ExtractMetadata(modelArtifactJSON []byte) (*ModelArtifact, error) {
	var modelArtifact ModelArtifact
	err := json.Unmarshal(modelArtifactJSON, &modelArtifact)
	if err != nil {
		return nil, fmt.Errorf("failed to unmarshal model artifact JSON: %w", err)
	}

	return &modelArtifact, nil
}

func StoreMetadata(db *sql.DB, modelArtifact *ModelArtifact) error {
	_, err := db.Exec(`
		INSERT INTO model_metadata (dataset_source, bias_metrics)
		VALUES ($1, $2)
	`, modelArtifact.DatasetSource, json.RawMessage(modelArtifact.BiasMetrics))
	if err != nil {
		return fmt.Errorf("failed to store metadata in database: %w", err)
	}

	return nil
}