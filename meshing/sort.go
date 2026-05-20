package meshing

import (
	"sort"
)

// ---------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------

// DeterministicSort orders a slice of groups in a fully deterministic way.
// It sorts **in‑place** and also returns the same slice for convenience.
//
// Ordering rules (applied in this exact order):
//   1️⃣  ID      – ascending (must be stable across runs)
//   2️⃣  Hash    – ascending (deterministic hash of the group's contents)
//   3️⃣  Priority– ascending (optional tie‑breaker, lower = earlier)
//
// The function uses sort.SliceStable so that elements that compare equal
// keep their original relative order – this guarantees stability for any
// future fields you might add.
//
// If your project already defines a different struct name or extra fields,
// simply adapt the type alias below – the sorting logic itself does not
// depend on any other package‑internal state.
func DeterministicSort(groups []Group) []Group {
	sort.SliceStable(groups, func(i, j int) bool {
		// 1️⃣ ID
		if groups[i].ID != groups[j].ID {
			return groups[i].ID < groups[j].ID
		}
		// 2️⃣ Hash
		if groups[i].Hash != groups[j].Hash {
			return groups[i].Hash < groups[j].Hash
		}
		// 3️⃣ Priority (optional)
		return groups[i].Priority < groups[j].Priority
	})
	return groups
}

// ---------------------------------------------------------------------
// Types – adapt if your code already defines them elsewhere
// ---------------------------------------------------------------------

// Group is the minimal representation required for deterministic sorting.
// If the real codebase already has a richer struct, you can either:
//   * embed this struct inside the real one, or
//   * replace this definition with a type alias:
//
//         type Group = yourpackage.RealGroup
//
// The three fields below **must be stable** (i.e. they never change
// during the lifetime of a pipeline run).  If you need additional
// tie‑breakers, add them after `Priority` and extend the comparison
// function accordingly.
type Group struct {
	ID       int64  // stable unique identifier
	Hash     uint64 // deterministic hash of the group's contents
	Priority int    // lower values sort earlier; optional
}