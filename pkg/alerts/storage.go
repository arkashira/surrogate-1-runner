package alerts

import "sync"

// Storage is a very small in‑memory store used for demo/testing.
// Replace with a DB, S3, or any other persistence layer.
type Storage interface {
	Save(r PersistedResult) error
	List() []PersistedResult
}

type memoryStore struct {
	mu   sync.RWMutex
	data []PersistedResult
}

func NewMemoryStore() Storage { return &memoryStore{} }

func (m *memoryStore) Save(r PersistedResult) error {
	m.mu.Lock()
	defer m.mu.Unlock()
	m.data = append(m.data, r)
	return nil
}

func (m *memoryStore) List() []PersistedResult {
	m.mu.RLock()
	defer m.mu.RUnlock()
	return append([]PersistedResult(nil), m.data...)
}