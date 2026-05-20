package main

import (
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/google/go-github/github"
	"github.com/xanzy/go-gitlab"
)

type CIWebhookPayload struct {
	Source      string                 `json:"source"`
	BuildStatus string                 `json:"build_status"`
	BuildNumber int                    `json:"build_number"`
	JobName     string                 `json:"job_name"`
	Commit      map[string]interface{} `json:"commit"`
}

type CIStatus struct {
	Status string `json:"status"`
}

var statusMap = map[string]string{
	"success": "completed",
	"failed":  "failed",
	"pending": "pending",
}

func handleCIWebhook(w http.ResponseWriter, r *http.Request) {
	var payload CIWebhookPayload
	err := json.NewDecoder(r.Body).Decode(&payload)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	switch r.Header.Get("X-GitHub-Event") {
	case "workflow_run":
		// Handle GitHub Actions
		go updateTaskStatus(payload, "github")
	case "Pipeline Hook":
		// Handle GitLab CI
		go updateTaskStatus(payload, "gitlab")
	default:
		http.Error(w, "Unsupported CI provider", http.StatusNotImplemented)
		return
	}

	w.WriteHeader(http.StatusOK)
}

func updateTaskStatus(payload CIWebhookPayload, provider string) {
	status := CIStatus{Status: "unknown"}

	switch provider {
	case "github":
		if payload.BuildStatus == "success" {
			status.Status = "success"
		} else {
			status.Status = "failure"
			triggerRetryNotification(payload.Commit["sha"].(string))
		}
	case "gitlab":
		if payload.BuildStatus == "success" {
			status.Status = "success"
		} else {
			status.Status = "failure"
			triggerRetryNotification(payload.Commit["author_name"].(string))
		}
	}

	fmt.Printf("CI status updated: %+v\n", status)
}

func triggerRetryNotification(assignee string) {
	fmt.Printf("Triggering retry notification for assignee: %s\n", assignee)
}

func main() {
	http.HandleFunc("/ci-webhook", handleCIWebhook)
	log.Println("Starting CI webhook server on :8080")
	http.ListenAndServe(":8080", nil)
}

// /opt/axentx/surrogate-1/src/ci_webhook_test.go
package main

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHandleCIWebhook(t *testing.T) {
	tests := []struct {
		eventType string
		payload   interface{}
	}{
		{"workflow_run", github.WorkflowRunEvent{}},
		{"Pipeline Hook", gitlab.PipelineHook{}},
	}

	for _, tt := range tests {
		t.Run(tt.eventType, func(t *testing.T) {
			jsonPayload, _ := json.Marshal(tt.payload)
			req := httptest.NewRequest("POST", "/ci-webhook", bytes.NewBuffer(jsonPayload))
			req.Header.Set("Content-Type", "application/json")
			req.Header.Set("X-GitHub-Event", tt.eventType)

			rr := httptest.NewRecorder()
			handleCIWebhook(rr, req)

			if status := rr.Code; status != http.StatusOK {
				t.Errorf("handler returned wrong status code: got %v want %v",
					status, http.StatusOK)
			}
		})
	}
}