package engine

import (
	"time"
)

func RetryWorkflow(workflow Workflow, maxRetries int) {
	for i := 0; i < maxRetries; i++ {
		ExecuteWorkflow(workflow)
		if workflow.Status != "failed" {
			break
		}
		time.Sleep(time.Duration(i+1) * time.Second)
	}
}