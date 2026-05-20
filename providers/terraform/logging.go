package terraform

import (
	"log"
	"time"
)

type WorkflowLog struct {
	ID        string    `json:"id"`
	Status    string    `json:"status"`
	Timestamp time.Time `json:"timestamp"`
}

func LogWorkflow(workflowID string, status string) {
	log.Printf("Workflow %s: %s at %v", workflowID, status, time.Now())
}

func NewWorkflowLog(workflowID string, status string) *WorkflowLog {
	return &WorkflowLog{
		ID:        workflowID,
		Status:    status,
		Timestamp: time.Now(),
	}
}