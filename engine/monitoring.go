package engine

import (
	"fmt"
	"time"
)

type Workflow struct {
	ID        string
	Name      string
	Status    string
	Timestamp time.Time
}

func MonitorWorkflowExecution(workflow Workflow) {
	fmt.Printf("Monitoring Workflow ID: %s, Name: %s, Status: %s, Timestamp: %v\n", workflow.ID, workflow.Name, workflow.Status, workflow.Timestamp)
}

func MonitorWorkflowFailure(workflow Workflow, err error) {
	fmt.Printf("Monitoring Workflow ID: %s, Name: %s failed with error: %v, Timestamp: %v\n", workflow.ID, workflow.Name, err, workflow.Timestamp)
}