package surrogate1

import (
	"testing"
)

func TestResourceAllocation(t *testing.T) {
	allocator := NewResourceAllocator(16, 32000) // 16 CPU cores, 32GB memory

	allocator.RegisterAgent("agent-1", Resource{CPU: 4, Memory: 8000})
	allocator.RegisterAgent("agent-2", Resource{CPU: 8, Memory: 16000})
	allocator.RegisterAgent("agent-3", Resource{CPU: 4, Memory: 8000})

	allocs := allocator.Monitor()
	if len(allocs) != 3 {
		t.Fatalf("expected 3 agents, got %d", len(allocs))
	}

	// Verify that total allocated CPU and memory do not exceed pool
	totalCPU := 0
	totalMem := 0
	for _, res := range allocs {
		totalCPU += res.CPU
		totalMem += res.Memory
	}
	if totalCPU > 16 || totalMem > 32000 {
		t.Fatalf("allocation exceeds pool: CPU %d, Mem %d", totalCPU, totalMem)
	}

	// Adjust agent-1 need and verify reallocation
	allocator.Adjust("agent-1", Resource{CPU: 6, Memory: 12000})
	allocs = allocator.Monitor()
	if allocs["agent-1"].CPU < 6 || allocs["agent-1"].Memory < 12000 {
		t.Fatalf("agent-1 not allocated enough resources after adjust: %+v", allocs["agent-1"])
	}

	// Deregister agent-2 and ensure remaining allocations adjust
	allocator.DeregisterAgent("agent-2")
	allocs = allocator.Monitor()
	if _, ok := allocs["agent-2"]; ok {
		t.Fatalf("agent-2 still present after deregistration")
	}
	if len(allocs) != 2 {
		t.Fatalf("expected 2 agents after deregistration, got %d", len(allocs))
	}
}