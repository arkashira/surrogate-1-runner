package models

import (
	"time"
)

type Task struct {
	ID          string    `json:"id"`
	Name        string    `json:"name"`
	Dependencies []string `json:"dependencies,omitempty"`
	Status      string    `json:"status"` // e.g., "pending", "running", "completed", "failed"
	CreatedAt   time.Time `json:"created_at"`
	UpdatedAt   time.Time `json:"updated_at"`
}