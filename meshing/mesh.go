package meshing

import (
	"encoding/binary"
	"errors"
	"fmt"
	"io"
	"sort"
	"strconv"
	"strings"
	"sync"
)

// -------------------------------------------------------------------
// Core geometry
// -------------------------------------------------------------------

// Vertex is a point in 3‑D space.
type Vertex struct {
	X, Y, Z float64
}

// Triangle references three vertices by their indices in the vertex slice.
type Triangle struct {
	A, B, C int
}

// -------------------------------------------------------------------
// Optional annotation elements (human‑readable lines)
// -------------------------------------------------------------------

// ElementKind enumerates the possible kinds of MeshElement.
type ElementKind int

const (
	KindVertex ElementKind = iota
	KindTriangle
	KindNode
	KindEdge
)

func (k ElementKind) String() string {
	switch k {
	case KindVertex:
		return "Vertex"
	case KindTriangle:
		return "Triangle"
	case KindNode:
		return "Node"
	case KindEdge:
		return "Edge"
	default:
		return "Unknown"
	}
}

// MeshElement is the unit that the generator pushes onto the output channel.
type MeshElement struct {
	Kind ElementKind // what the payload represents
	// Exactly one of the following fields is valid:
	Vertex   *Vertex
	Triangle *Triangle
	NodeID   int // for KindNode
	Edge     struct {
		From, To int
	}
}

// -------------------------------------------------------------------
// Errors
// -------------------------------------------------------------------
var (
	ErrEmptyInput       = errors.New("input data is empty")
	ErrInsufficientData = errors.New("input length must be a multiple of 12 bytes")
	ErrInvalidLine      = errors.New("invalid annotation line")
)