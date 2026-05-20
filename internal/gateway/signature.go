package gateway

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"net/http"
)

// MaskedRequest represents a request with masked signature
type MaskedRequest struct {
	OriginalRequest *http.Request
	MaskedSignature string
}

// GenerateMaskedSignature creates a masked signature for the given request
func GenerateMaskedSignature(req *http.Request) string {
	// Create a SHA256 hash of the request body
	bodyHash := sha256.Sum256(req.Body)
	// Convert the hash to a hex string
	hashString := hex.EncodeToString(bodyHash[:])

	// Create a new signature by combining the hash with a random string
	randomString := generateRandomString(16)
	maskedSignature := hashString + randomString

	return maskedSignature
}

// generateRandomString generates a random string of given length
func generateRandomString(length int) string {
	// Implementation of random string generation
	// ...
	return randomString
}

// MaskRequest masks the signature of the given request
func MaskRequest(req *http.Request) (*MaskedRequest, error) {
	maskedSignature := GenerateMaskedSignature(req)
	return &MaskedRequest{
		OriginalRequest: req,
		MaskedSignature: maskedSignature,
	}, nil
}