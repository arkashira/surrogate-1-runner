package admin

import (
	"encoding/json"
	"net/http"
	"strings"

	"github.com/axentx/surrogate-1/internal/access"
)

// SetToolAccessRequest represents the request payload for setting tool access
type SetToolAccessRequest struct {
	Roles []string `json:"roles"`
}

// SetToolAccessResponse represents the response from setting tool access
type SetToolAccessResponse struct {
	Success bool   `json:"success"`
	Message string `json:"message"`
}

// SetToolAccessHandler handles POST /admin/access/{tool}
// Payload: {"roles": ["admin","user"]}
// It overwrites the allowed role list for the specified tool
func SetToolAccessHandler(w http.ResponseWriter, r *http.Request) {
	// Auth middleware would verify admin privileges here
	// ...

	parts := strings.Split(strings.Trim(r.URL.Path, "/"), "/")
	if len(parts) < 3 {
		respondWithError(w, http.StatusBadRequest, "tool not specified")
		return
	}
	tool := parts[len(parts)-1]

	var req SetToolAccessRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		respondWithError(w, http.StatusBadRequest, "invalid json payload")
		return
	}

	// Convert string roles to Role type
	roles := make([]access.Role, len(req.Roles))
	for i, role := range req.Roles {
		roles[i] = access.Role(role)
	}

	// Set the roles
	access.GetDefaultRBAC().SetToolRoles(tool, roles)

	respondWithJSON(w, http.StatusOK, SetToolAccessResponse{
		Success: true,
		Message: "Tool access updated successfully",
	})
}

// Helper functions for API responses
func respondWithError(w http.ResponseWriter, code int, message string) {
	respondWithJSON(w, code, map[string]string{"error": message})
}

func respondWithJSON(w http.ResponseWriter, code int, payload interface{}) {
	response, _ := json.Marshal(payload)
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(code)
	w.Write(response)
}