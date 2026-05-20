package policy

import (
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"

	_ "github.com/lib/pq"
)

// Policy represents a CAROL policy
type Policy struct {
	ID          int    `json:"id"`
	Conditions  []Condition `json:"conditions"`
}

// Condition represents a condition in a CAROL policy
type Condition struct {
	DatasetProvenance string `json:"dataset_provenance"`
	ModelSize        int    `json:"model_size"`
}

// SavePolicy saves a policy to the database
func SavePolicy(db *sql.DB, policy Policy) error {
	_, err := db.Exec(`INSERT INTO policies (conditions) VALUES ($1)`, json.Marshal(policy.Conditions))
	if err != nil {
		return err
	}

	return nil
}

// GetPolicy retrieves a policy from the database
func GetPolicy(db *sql.DB, id int) (Policy, error) {
	var policy Policy
	err := db.QueryRow(`SELECT conditions FROM policies WHERE id = $1`, id).Scan(&policy.Conditions)
	if err != nil {
		return policy, err
	}

	return policy, nil
}