package api

import (
	"encoding/json"
	"log"
	"net/http"
)

// Request represents the structure of the API request
type Request struct {
	ChainID string `json:"chain_id"`
	// Other fields...
}

// Relay handles the incoming requests
func Relay(w http.ResponseWriter, r *http.Request) {
	var req Request
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	// Validate chain ID
	if !isChainIDValid(req.ChainID) {
		http.Error(w, "Invalid chain ID", http.StatusBadRequest)
		return
	}

	// Log the chain routing decision
	log.Printf("Routing transaction to chain: %s", req.ChainID)

	// Process the request...
	// Other logic...
}

// isChainIDValid checks if the chain ID is in the whitelist
func isChainIDValid(chainID string) bool {
	// Define the whitelist of valid chain IDs
	validChains := map[string]bool{
		"1":  true, // Ethereum Mainnet
		"5":  true, // Goerli Testnet
		"137": true, // Polygon Mainnet
		// Add other valid chains as needed
	}

	return validChains[chainID]
}