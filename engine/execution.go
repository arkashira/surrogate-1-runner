package engine

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/axentx/surrogate-1-training-pairs/axentx"
)

// WorkflowExecutionEngine represents the workflow execution engine
type WorkflowExecutionEngine struct {
	workflows []Workflow
	logger    *log.Logger
}

// Workflow represents a workflow
type Workflow struct {
	Name    string
	Steps   []Step
	Retry   int
	Timeout time.Duration
}

// Step represents a step in a workflow
type Step struct {
	Name    string
	Command string
}

// NewWorkflowExecutionEngine returns a new workflow execution engine
func NewWorkflowExecutionEngine(workflows []Workflow) *WorkflowExecutionEngine {
	return &WorkflowExecutionEngine{
		workflows: workflows,
		logger:    log.New(log.Writer(), "workflow-execution-engine: ", log.Ldate|log.Ltime|log.Lshortfile),
	}
}

// ExecuteWorkflows executes the workflows in the order they are defined
func (e *WorkflowExecutionEngine) ExecuteWorkflows(ctx context.Context) {
	for _, workflow := range e.workflows {
		e.executeWorkflow(ctx, workflow)
	}
}

// executeWorkflow executes a single workflow
func (e *WorkflowExecutionEngine) executeWorkflow(ctx context.Context, workflow Workflow) {
	for attempt := 0; attempt <= workflow.Retry; attempt++ {
		startTime := time.Now()
		e.logger.Printf("Starting workflow %s (attempt %d)", workflow.Name, attempt)
		for _, step := range workflow.Steps {
			if err := e.executeStep(ctx, step); err != nil {
				e.logger.Printf("Error executing step %s in workflow %s: %v", step.Name, workflow.Name, err)
				if attempt < workflow.Retry {
					e.logger.Printf("Retrying workflow %s in %v", workflow.Name, workflow.Timeout)
					time.Sleep(workflow.Timeout)
				} else {
					e.logger.Printf("Failed to execute workflow %s after %d attempts", workflow.Name, workflow.Retry)
					return
				}
			}
		}
		e.logger.Printf("Completed workflow %s in %v", workflow.Name, time.Since(startTime))
		return
	}
}

// executeStep executes a single step in a workflow
func (e *WorkflowExecutionEngine) executeStep(ctx context.Context, step Step) error {
	// Execute the command
	cmd := fmt.Sprintf("sh -c '%s'", step.Command)
	_, err := axentx.RunCommand(ctx, cmd)
	return err
}