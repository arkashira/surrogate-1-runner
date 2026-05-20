package api

import (
	"encoding/json"
	"net/http"

	"github.com/google/uuid"
)

// taskRequest represents the JSON payload for creating a new task.
type taskRequest struct {
	Task         string   `json:"task"`
	Dependencies []string `json:"dependencies"`
}

// taskResponse represents the JSON response returned to the client.
type taskResponse struct {
	TaskID string `json:"task_id"`
	Status string `json:"status"`
}

// taskHandler handles POST /tasks requests.
// It accepts a JSON body with the task name and an optional list of dependency IDs,
// creates a new task, and returns the task ID and initial status.
func taskHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method != http.MethodPost {
		http.Error(w, "method not allowed", http.StatusMethodNotAllowed)
		return
	}

	var req taskRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		http.Error(w, "invalid request body", http.StatusBadRequest)
		return
	}
	if req.Task == "" {
		http.Error(w, "task name required", http.StatusBadRequest)
		return
	}

	// Generate a unique ID for the task
	taskID := uuid.New().String()

	// Create the task in the manager
	task, err := taskManager.SubmitTask(taskID, req.Task, req.Dependencies)
	if err != nil {
		http.Error(w, "failed to submit task", http.StatusInternalServerError)
		return
	}

	resp := taskResponse{
		TaskID: task.ID,
		Status: task.Status,
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}