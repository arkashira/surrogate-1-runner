package handlers

import (
	"encoding/json"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/go-chi/jwtauth"
	"github.com/go-chi/cors"
	"github.com/go-chi/render"
	"github.com/axentx/surrogate-1/internal/models"
	"github.com/axentx/surrogate-1/internal/database"
)

// CreateTask handles creating a new task with optional dependencies
func CreateTask(w http.ResponseWriter, r *http.Request) {
	w.Header().Set("Content-Type", "application/json")
	w.Header().Set("Access-Control-Allow-Origin", "*")

	var task models.Task
	if err := json.NewDecoder(r.Body).Decode(&task); err != nil {
		render.Status(r, http.StatusBadRequest)
		render.JSON(w, r, map[string]string{"error": "invalid request body"})
		return
	}

	// Validate and store dependencies if provided
	if len(task.Dependencies) > 0 {
		// In a real implementation, validate dependencies exist in DB
		// For this feature, we simply store the provided IDs
	}

	// Set timestamps and initial status
	task.CreatedAt = time.Now()
	task.UpdatedAt = time.Now()
	task.Status = "pending"

	// Save task to database
	if err := database.SaveTask(task); err != nil {
		render.Status(r, http.StatusInternalServerError)
		render.JSON(w, r, map[string]string{"error": "failed to save task"})
		return
	}

	// Return success response with task ID and status
	render.Status(r, http.StatusCreated)
	render.JSON(w, r, map[string]interface{}{
		"task_id": task.ID,
		"status":  task.Status,
	})
}