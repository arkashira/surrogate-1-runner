package api

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"
	"os"
	"time"
)

type Transaction struct {
	ID        string    `json:"id"`
	Status    string    `json:"status"`
	Chain     string    `json:"chain"`
	Latency   int       `json:"latency_ms"`
	Timestamp time.Time `json:"timestamp"`
}

func HistoryHandler(w http.ResponseWriter, r *http.Request) {
	// JWT validation (simplified for example)
	authHeader := r.Header.Get("Authorization")
	if authHeader != "Bearer "+os.Getenv("DASHBOARD_JWT") {
		http.Error(w, "Unauthorized", http.StatusUnauthorized)
		return
	}

	db, err := sql.Open("postgres", os.Getenv("DATABASE_DSN"))
	if err != nil {
		http.Error(w, "Database connection failed", http.StatusInternalServerError)
		return
	}
	defer db.Close()

	rows, err := db.Query(`
		SELECT id, status, chain, latency, timestamp 
		FROM transactions 
		ORDER BY timestamp DESC 
		LIMIT 100
	`)
	if err != nil {
		http.Error(w, fmt.Sprintf("Query failed: %v", err), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	var transactions []Transaction
	for rows.Next() {
		var t Transaction
		if err := rows.Scan(&t.ID, &t.Status, &t.Chain, &t.Latency, &t.Timestamp); err != nil {
			http.Error(w, fmt.Sprintf("Scan failed: %v", err), http.StatusInternalServerError)
			return
		}
		transactions = append(transactions, t)
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(transactions); err != nil {
		http.Error(w, fmt.Sprintf("Encode failed: %v", err), http.StatusInternalServerError)
	}
}