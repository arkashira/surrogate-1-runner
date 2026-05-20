package api

import (
	"encoding/json"
	"errors"
	"io"
	"net/http"
	"strings"
)

type RelayRequest struct {
	SignedTransaction string `json:"signed_transaction"`
	ChainID           uint64 `json:"chain_id"`
}

func ValidateRelayRequest(r *http.Request) error {
	// Check content type
	if r.Header.Get("Content-Type") != "application/json" {
		return errors.New("invalid content type: must be application/json")
	}

	// Read and parse body
	body, err := io.ReadAll(r.Body)
	if err != nil {
		return errors.New("failed to read request body")
	}
	if len(body) == 0 {
		return errors.New("empty request body")
	}

	var req RelayRequest
	if err := json.Unmarshal(body, &req); err != nil {
		return errors.New("malformed JSON: " + err.Error())
	}

	// Validate required fields
	if req.SignedTransaction == "" {
		return errors.New("missing required field: signed_transaction")
	}
	if req.ChainID == 0 {
		return errors.New("missing required field: chain_id")
	}

	return nil
}

func RelayValidationMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		if err := ValidateRelayRequest(r); err != nil {
			http.Error(w, 
				strings.Join([]string{
					"Request validation failed: ", 
					err.Error(),
				}, ""), 
				http.StatusBadRequest)
			return
		}
		next.ServeHTTP(w, r)
	})
}