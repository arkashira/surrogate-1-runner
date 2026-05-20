package api

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/axentx/surrogate-1/database"
)

func TestAlertHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	projectID := vars["projectID"]

	if projectID == "" {
		http.Error(w, "project ID is required", http.StatusBadRequest)
		return
	}

	config, err := database.GetAlertConfig(projectID)
	if err != nil {
		http.Error(w, err.Error(), http.StatusNotFound)
		return
	}

	alert := &database.Alert{
		ProjectID: projectID,
		Threshold: config.BudgetLimit,
	}

	if err := sendTestAlert(alert, config.WebhookURLs); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(map[string]string{
		"status":  "success",
		"message": "test alert sent",
	})
}

func sendTestAlert(alert *database.Alert, webhookURLs []string) error {
	for _, url := range webhookURLs {
		body, _ := json.Marshal(alert)
		resp, err := http.Post(url, "application/json", nil)
		if err != nil {
			return fmt.Errorf("failed to POST to %s: %w", url, err)
		}
		defer resp.Body.Close()
		io.Copy(io.Discard, resp.Body) // drain body to enable connection reuse

		if resp.StatusCode >= 400 {
			return fmt.Errorf("webhook %s returned status %d", url, resp.StatusCode)
		}
	}
	return nil
}