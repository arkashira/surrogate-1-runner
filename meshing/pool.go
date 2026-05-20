package meshing

import (
	"sync"
)

// Node is the basic element used during mesh generation.
// Keep it lightweight – the pool shines when the struct is cheap to allocate
// but may contain reference‑heavy sub‑structures (slices, maps, child nodes,
// etc.) that we want to recycle without triggering the GC on every use.
type Node struct {
	// Example scalar fields
	ID       int
	Position [3]float64

	// Example reference‑heavy fields – they are deliberately simple here
	// but in the real code they may hold vertex buffers, adjacency lists,
	// etc.
	Children []*Node
	// Add other slices / maps here and remember to nil‑them in Reset().
}

// Reset clears the node so that it does not retain references to previously
// stored data.  Call this before putting the node back into the pool.
func (n *Node) Reset() {
	n.ID = 0
	n.Position = [3]float64{}
	n.Children = nil
	// If you add more reference‑type members, nil‑them here:
	// n.Vertices = nil
	// n.Attributes = nil
}

// Global pool – a single instance is sufficient because sync.Pool is already
// sharded internally and works well across goroutines.
var nodePool = sync.Pool{
	New: func() interface{} {
		// Allocate a fresh, zeroed Node.
		return &Node{}
	},
}

// AcquireNode fetches a *Node from the pool and guarantees that it is in a
// clean state.  The caller may treat the returned value as a freshly allocated
// object.
func AcquireNode() *Node {
	n := nodePool.Get().(*Node)
	// The pool may hand us a reused node that still contains stale data.
	// Reset it to the zero value before handing it out.
	n.Reset()
	return n
}

// ReleaseNode returns a *Node to the pool after clearing its contents.
// The node must not be used after this call.
func ReleaseNode(n *Node) {
	if n == nil {
		return
	}
	n.Reset()
	nodePool.Put(n)
}