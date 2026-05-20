package lineage

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"
)

// Graph represents a simple adjacency list of lineage nodes.
// Nodes can be datasets, transformation jobs, or model versions.
type Graph struct {
	Adjacency map[string][]string
}

// NewGraph creates a sample lineage graph.
// In a real implementation this would query a database or metadata store.
func NewGraph() *Graph {
	return &Graph{
		Adjacency: map[string][]string{
			"dataset_1": {"job_1"},
			"dataset_2": {"job_2"},
			"job_1":     {"model_1"},
			"job_2":     {"model_1"},
			"model_1":   {"model_2"},
			"model_2":   {},
		},
	}
}

// GetLineageHandler returns the adjacency list for the requested model_id.
// The response format is:
//   { "adjacency": { "node": ["child1", "child2"], ... } }
func GetLineageHandler(w http.ResponseWriter, r *http.Request) {
	modelID := r.URL.Query().Get("model_id")
	if modelID == "" {
		http.Error(w, "model_id query param required", http.StatusBadRequest)
		return
	}

	graph := NewGraph()

	// Filter the graph to only include nodes reachable from the requested model.
	adj := pruneGraph(graph.Adjacency, modelID)

	resp := map[string]map[string][]string{
		"adjacency": adj,
	}

	w.Header().Set("Content-Type", "application/json")
	if err := json.NewEncoder(w).Encode(resp); err != nil {
		http.Error(w, fmt.Sprintf("encoding error: %v", err), http.StatusInternalServerError)
		return
	}
}

// ExportDOTHandler returns the lineage graph in DOT format.
// The DOT file contains all nodes and edges reachable from the requested model.
func ExportDOTHandler(w http.ResponseWriter, r *http.Request) {
	modelID := r.URL.Query().Get("model_id")
	if modelID == "" {
		http.Error(w, "model_id query param required", http.StatusBadRequest)
		return
	}

	graph := NewGraph()
	adj := pruneGraph(graph.Adjacency, modelID)

	var sb strings.Builder
	sb.WriteString("digraph lineage {\n")
	for node, children := range adj {
		if len(children) == 0 {
			sb.WriteString(fmt.Sprintf("  \"%s\";\n", node))
		}
		for _, child := range children {
			sb.WriteString(fmt.Sprintf("  \"%s\" -> \"%s\";\n", node, child))
		}
	}
	sb.WriteString("}\n")

	w.Header().Set("Content-Type", "text/plain")
	w.Header().Set("Content-Disposition", "attachment; filename=\"lineage.dot\"")
	if _, err := w.Write([]byte(sb.String())); err != nil {
		http.Error(w, fmt.Sprintf("write error: %v", err), http.StatusInternalServerError)
		return
	}
}

// RegisterRoutes adds the lineage endpoints to the provided ServeMux.
func RegisterRoutes(mux *http.ServeMux) {
	mux.HandleFunc("/api/lineage", GetLineageHandler)
	mux.HandleFunc("/api/lineage/export", ExportDOTHandler)
}

// pruneGraph returns a subgraph containing only nodes reachable from start.
// It performs a simple DFS.
func pruneGraph(adj map[string][]string, start string) map[string][]string {
	visited := make(map[string]bool)
	stack := []string{start}
	result := make(map[string][]string)

	for len(stack) > 0 {
		n := stack[len(stack)-1]
		stack = stack[:len(stack)-1]
		if visited[n] {
			continue
		}
		visited[n] = true
		children := adj[n]
		result[n] = children
		for _, c := range children {
			if !visited[c] {
				stack = append(stack, c)
			}
		}
	}
	return result
}