package surrogate1

import (
	"sync"
	"time"
)

// Resource represents CPU cores and memory in megabytes.
type Resource struct {
	CPU    int // number of CPU cores
	Memory int // memory in MB
}

// SurrogateAgent holds the current resource need and allocation for an agent.
type SurrogateAgent struct {
	ID          string
	Need        Resource
	Allocated   Resource
	LastUpdated time.Time
}

// ResourceAllocator manages resource distribution across surrogate-1 agents.
type ResourceAllocator struct {
	mu          sync.Mutex
	agents      map[string]*SurrogateAgent
	totalCPU    int
	totalMemory int
}

// NewResourceAllocator creates a new allocator with the total pool of resources.
func NewResourceAllocator(totalCPU, totalMemory int) *ResourceAllocator {
	return &ResourceAllocator{
		agents:      make(map[string]*SurrogateAgent),
		totalCPU:    totalCPU,
		totalMemory: totalMemory,
	}
}

// RegisterAgent registers a new agent with its resource need and triggers allocation.
func (ra *ResourceAllocator) RegisterAgent(id string, need Resource) {
	ra.mu.Lock()
	defer ra.mu.Unlock()
	ra.agents[id] = &SurrogateAgent{
		ID:          id,
		Need:        need,
		Allocated:   Resource{CPU: 0, Memory: 0},
		LastUpdated: time.Now(),
	}
	ra.allocate()
}

// allocate distributes resources proportionally based on declared needs.
func (ra *ResourceAllocator) allocate() {
	totalNeededCPU := 0
	totalNeededMemory := 0
	for _, a := range ra.agents {
		totalNeededCPU += a.Need.CPU
		totalNeededMemory += a.Need.Memory
	}
	if totalNeededCPU == 0 || totalNeededMemory == 0 {
		return
	}
	for _, a := range ra.agents {
		cpuShare := a.Need.CPU * ra.totalCPU / totalNeededCPU
		memShare := a.Need.Memory * ra.totalMemory / totalNeededMemory
		a.Allocated = Resource{CPU: cpuShare, Memory: memShare}
		a.LastUpdated = time.Now()
	}
}

// Monitor returns the current allocation map for all agents.
func (ra *ResourceAllocator) Monitor() map[string]Resource {
	ra.mu.Lock()
	defer ra.mu.Unlock()
	result := make(map[string]Resource)
	for id, a := range ra.agents {
		result[id] = a.Allocated
	}
	return result
}

// Adjust updates the resource need for a specific agent and re‑allocates.
func (ra *ResourceAllocator) Adjust(id string, newNeed Resource) {
	ra.mu.Lock()
	defer ra.mu.Unlock()
	if a, ok := ra.agents[id]; ok {
		a.Need = newNeed
		a.LastUpdated = time.Now()
		ra.allocate()
	}
}

// DeregisterAgent removes an agent from the allocator and re‑allocates remaining resources.
func (ra *ResourceAllocator) DeregisterAgent(id string) {
	ra.mu.Lock()
	defer ra.mu.Unlock()
	delete(ra.agents, id)
	ra.allocate()
}