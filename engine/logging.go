package engine

import (
	"log"
	"time"
)

type Workflow struct {
	ID        string
	Name      string
	Status    string
	Timestamp time.Time
}

func LogWorkflowExecution(workflow Workflow) {
	log.Printf("Workflow ID: %s, Name: %s, Status: %s, Timestamp: %v", workflow.ID, workflow.Name, workflow.Status, workflow.Timestamp)
}

func LogWorkflowFailure(workflow Workflow, err error) {
	log.Printf("Workflow ID: %s, Name: %s failed with error: %v, Timestamp: %v", workflow.ID, workflow.Name, err, workflow.Timestamp)
}