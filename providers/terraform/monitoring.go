package terraform

import (
	"fmt"
	"time"
)

type WorkflowMonitor struct {
	ID        string    `json:"id"`
	Status    string    `json:"status"`
	Timestamp time.Time `json:"timestamp"`
}

func MonitorWorkflow(workflowID string, status string) {
	fmt.Printf("Monitoring Workflow %s: %s at %v\n", workflowID, status, time.Now())
}

func NewWorkflowMonitor(workflowID string, status string) *WorkflowMonitor {
	return &WorkflowMonitor{
		ID:        workflowID,
		Status:    status,
		Timestamp: time.Now(),
	}
}