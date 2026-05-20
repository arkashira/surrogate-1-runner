package relay

import (
	"encoding/json"
	"net/http"
)

type TransactionRequest struct {
	ChainID string `json:"chain_id"`
}

// HandleTransactionRequest handles incoming transaction requests.
func HandleTransactionRequest(w http.ResponseWriter, r *http.Request) {
	var req TransactionRequest
	err := json.NewDecoder(r.Body).Decode(&req)
	if err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}

	err = RouteTransaction(req.ChainID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusOK)
	w.Write([]byte("Transaction processed successfully"))
}