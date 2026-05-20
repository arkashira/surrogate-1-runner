package engine

import (
	"sync"
	"time"

	"github.com/google/uuid"
)

type JobStore struct {
	jobs map[string]*Job
	mu   sync.RWMutex
}

type Job struct {
	ID        string
	Status    string
	CreatedAt time.Time
	CompletedAt time.Time
}

func NewJobStore() *JobStore {
	return &JobStore{
		jobs: make(map[string]*Job),
	}
}

func (js *JobStore) GetJob(id string) (*Job, error) {
	js.mu.RLock()
	defer js.mu.RUnlock()
	job, ok := js.jobs[id]
	if !ok {
		return nil, ErrJobNotFound
	}
	return job, nil
}

func (js *JobStore) SetJob(job *Job) {
	js.mu.Lock()
	defer js.mu.Unlock()
	js.jobs[job.ID] = job
}

func (js *JobStore) DeleteJob(id string) {
	js.mu.Lock()
	defer js.mu.Unlock()
	delete(js.jobs, id)
}

const (
	ErrJobNotFound = "job not found"
)

type TTLJobStore struct {
	*JobStore
	ttl time.Duration
}

func NewTTLJobStore(ttl time.Duration) *TTLJobStore {
	return &TTLJobStore{
		JobStore: NewJobStore(),
		ttl:      ttl,
	}
}

func (tjs *TTLJobStore) Cleanup() {
	tjs.mu.Lock()
	defer tjs.mu.Unlock()
	now := time.Now()
	for id, job := range tjs.jobs {
		if job.CompletedAt.Add(tjs.ttl).Before(now) {
			delete(tjs.jobs, id)
		}
	}
}