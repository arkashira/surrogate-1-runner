package dashboard

import (
	"encoding/json"
	"net/http"
	"sync"

	"github.com/gorilla/mux"
)

// Action represents an external action that has been pinned.
type Action struct {
	Name string `json:"name"`
	SHA  string `json:"sha"`
}

// ComplianceStore holds the pinned actions in memory.
// In a real system this would be backed by a database or persistent store.
type ComplianceStore struct {
	mu      sync.RWMutex
	actions map[string]Action
}

// NewComplianceStore creates a new in-memory store.
func NewComplianceStore() *ComplianceStore {
	return &ComplianceStore{
		actions: make(map[string]Action),
	}
}

// PinAction adds or updates a pinned action.
func (cs *ComplianceStore) PinAction(name, sha string) {
	cs.mu.Lock()
	defer cs.mu.Unlock()
	cs.actions[name] = Action{Name: name, SHA: sha}
}

// GetAll returns all pinned actions.
func (cs *ComplianceStore) GetAll() []Action {
	cs.mu.RLock()
	defer cs.mu.RUnlock()
	result := make([]Action, 0, len(cs.actions))
	for _, a := range cs.actions {
		result = append(result, a)
	}
	return result
}

// RollbackAction removes a pinned action by name.
func (cs *ComplianceStore) RollbackAction(name string) {
	cs.mu.Lock()
	defer cs.mu.Unlock()
	delete(cs.actions, name)
}

// ComplianceHandler handles HTTP requests for the compliance dashboard.
type ComplianceHandler struct {
	store *ComplianceStore
}

// NewComplianceHandler creates a new handler with the given store.
func NewComplianceHandler(store *ComplianceStore) *ComplianceHandler {
	return &ComplianceHandler{store: store}
}

// ServeHTTP implements http.Handler.
// It routes based on the request method and URL path.
func (ch *ComplianceHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	switch {
	case r.Method == http.MethodGet && r.URL.Path == "/compliance":
		ch.handleGetAll(w, r)
	case r.Method == http.MethodPost && r.URL.Path == "/compliance/pin":
		ch.handlePin(w, r)
	case r.Method == http.MethodPost && r.URL.Path == "/compliance/rollback":
		ch.handleRollback(w, r)
	default:
		http.NotFound(w, r)
	}
}

// handleGetAll returns all pinned actions as JSON.
func (ch *ComplianceHandler) handleGetAll(w http.ResponseWriter, r *http.Request) {
	actions := ch.store.GetAll()
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(actions)
}

// handlePin pins a new action. Expects JSON body: {"name":"action","sha":"abcd1234"}.
func (ch *ComplianceHandler) handlePin(w http.ResponseWriter, r *http.Request) {
	var a Action
	if err := json.NewDecoder(r.Body).Decode(&a); err != nil {
		http.Error(w, "invalid request body", http.StatusBadRequest)
		return
	}
	if a.Name == "" || a.SHA == "" {
		http.Error(w, "name and sha required", http.StatusBadRequest)
		return
	}
	ch.store.PinAction(a.Name, a.SHA)
	w.WriteHeader(http.StatusCreated)
}

// handleRollback removes a pinned action. Expects JSON body: {"name":"action"}.
func (ch *ComplianceHandler) handleRollback(w http.ResponseWriter, r *http.Request) {
	var payload struct{ Name string `json:"name"` }
	if err := json.NewDecoder(r.Body).Decode(&payload); err != nil {
		http.Error(w, "invalid request body", http.StatusBadRequest)
		return
	}
	if payload.Name == "" {
		http.Error(w, "name required", http.StatusBadRequest)
		return
	}
	ch.store.RollbackAction(payload.Name)
	w.WriteHeader(http.StatusOK)
}

// RegisterRoutes registers the compliance routes on the provided router.
func RegisterRoutes(router *mux.Router, store *ComplianceStore) {
	handler := NewComplianceHandler(store)
	router.Handle("/compliance", handler).Methods(http.MethodGet)
	router.Handle("/compliance/pin", handler).Methods(http.MethodPost)
	router.Handle("/compliance/rollback", handler).Methods(http.MethodPost)
}