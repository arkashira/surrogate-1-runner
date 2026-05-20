package api

import (
	"encoding/json"
	"net/http"
	"log"
	"time"
	"github.com/gorilla/mux"
	"surrogate-1/workflows"
)

type WebhookPayload struct {
	Event     string                 `json:"event"`
	Workflow  string                 `json:"workflow"`
	Status    string                 `json:"status"`
	Data      map[string]interface{} `json:"data"`
}

func WebhookHandler(w http.ResponseWriter, r *http.Request) {
	var payload WebhookPayload
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	// Log the webhook event
	log.Printf("Received webhook event: %s for workflow: %s", payload.Event, payload.Workflow)

	// Trigger the appropriate workflow
	switch payload.Event {
	case "workflow_trigger":
		go triggerWorkflow(payload.Workflow, payload.Data)
	case "status_update":
		go updateWorkflowStatus(payload.Workflow, payload.Status)
	default:
		http.Error(w, "Unknown event type", http.StatusBadRequest)
		return
	}

	w.WriteHeader(http.StatusAccepted)
}

func triggerWorkflow(workflow string, data map[string]interface{}) {
	// Implement workflow triggering logic
	log.Printf("Triggering workflow: %s", workflow)
	workflows.TriggerWorkflow(workflow, data)
}

func updateWorkflowStatus(workflow string, status string) {
	// Implement status update logic
	log.Printf("Updating status for workflow: %s to %s", workflow, status)
	workflows.UpdateWorkflowStatus(workflow, status)
}

func RegisterWebhookRoutes(router *mux.Router) {
	router.HandleFunc("/webhooks", WebhookHandler).Methods("POST")
}