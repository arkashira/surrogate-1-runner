package engine

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/axentx/surrogate-1-training-pairs/axentx"
)

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

// NewWorkflow returns a new workflow
func NewWorkflow(name string, steps []Step, retry int, timeout time.Duration) Workflow {
	return Workflow{
		Name:    name,
		Steps:   steps,
		Retry:   retry,
		Timeout: timeout,
	}
}

// NewStep returns a new step
func NewStep(name string, command string) Step {
	return Step{
		Name:    name,
		Command: command,
	}
}