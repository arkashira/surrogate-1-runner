package engine

import (
	"testing"
	"time"

	"github.com/google/uuid"
)

func TestTTLJobStoreCleanup(t *testing.T) {
	tjs := NewTTLJobStore(1 * time.Hour)
	job := &Job{
		ID:        uuid.NewString(),
		Status:    "completed",
		CreatedAt: time.Now(),
		CompletedAt: time.Now().Add(-1 * time.Hour),
	}
	tjs.SetJob(job)
	tjs.Cleanup()
	if _, ok := tjs.GetJob(job.ID); ok {
		t.Errorf("expected job to be deleted")
	}
}