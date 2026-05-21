package policy

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/http"

	"github.com/go-playground/validator/v10"
	"github.com/gorilla/mux"
)

// Policy represents a JSON policy
type Policy struct {
	Packages []Package `json:"packages"`
}

// Package represents a Windows package
type Package struct {
	Name    string `json:"name"`
	Version string `json:"version"`
}

// ValidatePolicy validates a policy against the JSON schema
func ValidatePolicy(policy Policy) error {
	schemaBytes, err := ioutil.ReadFile("/opt/axentx/surrogate-1/policy/schema.json")
	if err != nil {
		return fmt.Errorf("failed to read schema file: %w", err)
	}

	var schema map[string]interface{}
	err = json.Unmarshal(schemaBytes, &schema)
	if err != nil {
		return fmt.Errorf("failed to unmarshal schema: %w", err)
	}

	validate := validator.New()
	err = validate.Struct(policy)
	if err != nil {
		return fmt.Errorf("policy validation failed: %w", err)
	}

	return nil
}

// PolicyValidationMiddleware is a middleware that validates policies
func PolicyValidationMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		var policy Policy
		err := json.NewDecoder(r.Body).Decode(&policy)
		if err != nil {
			http.Error(w, "invalid JSON", http.StatusBadRequest)
			return
		}

		err = ValidatePolicy(policy)
		if err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		next.ServeHTTP(w, r)
	})
}