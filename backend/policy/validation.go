package policy

import (
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"

	"github.com/go-playground/validator/v10"
	"github.com/thedevsaddam/govalidator"
)

// JSONSchema represents a JSON schema for validation
type JSONSchema struct {
	Schema string `json:"schema"`
}

// ValidateJSON validates a JSON payload against a schema
func ValidateJSON(payload []byte, schema string) error {
	validate := validator.New()
	err := validate.Schema(schema)
	if err != nil {
		return err
	}

	var data map[string]interface{}
	err = json.Unmarshal(payload, &data)
	if err != nil {
		return err
	}

	_, err = govalidator.ValidateMap(data, schema)
	if err != nil {
		return err
	}

	return nil
}

// JSONValidationMiddleware is a middleware that validates JSON payloads
func JSONValidationMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			next.ServeHTTP(w, r)
			return
		}

		var payload map[string]interface{}
		err := json.NewDecoder(r.Body).Decode(&payload)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		schema := `{
			"type": "object",
			"properties": {
				"conditions": {
					"type": "array",
					"items": {
						"type": "object",
						"properties": {
							"dataset_provenance": {"type": "string"},
							"model_size": {"type": "integer"}
						},
						"required": ["dataset_provenance", "model_size"]
					}
				}
			},
			"required": ["conditions"]
		}`

		err = ValidateJSON([]byte(schema), schema)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		next.ServeHTTP(w, r)
	})
}