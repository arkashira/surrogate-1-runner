package meshing

import (
	"encoding/binary"
	"io"
)

// GenerateMeshFromReader reads a binary stream of 12‑byte vertex records.
// It returns a *Mesh* (all vertices + triangles) **and** a channel that streams
// the same data as MeshElements.  The channel is closed when the function returns.
func GenerateMeshFromReader(r io.Reader) (*Mesh, <-chan MeshElement, error) {
	// Fast‑path: if r implements io.ReaderAt we can pre‑size slices.
	var (
		vertices  []Vertex
		triangles []Triangle
		elements  = make(chan MeshElement, 1024) // buffered for throughput
	)

	// Helper to push a vertex onto the channel.
	pushVertex := func(v Vertex, idx int) {
		elements <- MeshElement{
			Kind:   KindVertex,
			Vertex: &v,
		}
		// Every third vertex creates a triangle.
		if (idx+1)%3 == 0 {
			tri := Triangle{
				A: idx - 2,
				B: idx - 1,
				C: idx,
			}
			triangles = append(triangles, tri)
			elements <- MeshElement{
				Kind:     KindTriangle,
				Triangle: &tri,
			}
		}
	}

	// ----------------------------------------------------------------
	// 1️⃣  Read the stream in 12‑byte blocks.
	// ----------------------------------------------------------------
	const blockSize = 12
	buf := make([]byte, blockSize)
	idx := 0
	for {
		_, err := io.ReadFull(r, buf)
		if err == io.EOF {
			break // normal termination – no more data
		}
		if err == io.ErrUnexpectedEOF {
			// Not a full vertex record → malformed input.
			close(elements)
			return nil, nil, ErrInsufficientData
		}
		if err != nil {
			close(elements)
			return nil, nil, fmt.Errorf("read error: %w", err)
		}

		// Decode little‑endian uint32 → float64.
		x := float64(binary.LittleEndian.Uint32(buf[0:4]))
		y := float64(binary.LittleEndian.Uint32(buf[4:8]))
		z := float64(binary.LittleEndian.Uint32(buf[8:12]))
		v := Vertex{X: x, Y: y, Z: z}
		vertices = append(vertices, v)
		pushVertex(v, idx)
		idx++
	}
	close(elements)

	if len(vertices) == 0 {
		return nil, nil, ErrEmptyInput
	}
	return &Mesh{Vertices: vertices, Triangles: triangles}, elements, nil
}