package access

import (
	"errors"
	"sync"
)

// Role represents a user role in the system
type Role string

const (
	RoleAdmin Role = "admin"
	RoleUser  Role = "user"
	RoleGuest Role = "guest" // Added for more granular control
)

// RBAC implements role-based access control for tools
type RBAC struct {
	toolRoles map[string]map[Role]struct{}
	mu        sync.RWMutex
}

// NewRBAC creates a new RBAC instance with default configurations
func NewRBAC() *RBAC {
	rbac := &RBAC{
		toolRoles: make(map[string]map[Role]struct{}),
	}

	// Default configurations
	rbac.SetToolRoles("basic-tools", []Role{RoleUser, RoleAdmin})
	rbac.SetToolRoles("admin-tools", []Role{RoleAdmin})

	return rbac
}

// SetToolRoles configures which roles may access a given tool
func (r *RBAC) SetToolRoles(tool string, roles []Role) {
	r.mu.Lock()
	defer r.mu.Unlock()

	roleSet := make(map[Role]struct{})
	for _, role := range roles {
		roleSet[role] = struct{}{}
	}
	r.toolRoles[tool] = roleSet
}

// GetToolRoles returns the roles allowed for a tool
func (r *RBAC) GetToolRoles(tool string) ([]Role, error) {
	r.mu.RLock()
	defer r.mu.RUnlock()

	set, ok := r.toolRoles[tool]
	if !ok {
		return nil, errors.New("tool not found in RBAC configuration")
	}

	roles := make([]Role, 0, len(set))
	for role := range set {
		roles = append(roles, role)
	}
	return roles, nil
}

// UserRoles returns the roles associated with a user
func (r *RBAC) UserRoles(userID string) ([]Role, error) {
	// In production, this would integrate with your auth system
	// For now, we'll implement a simple fallback
	if userID == "" {
		return []Role{RoleGuest}, nil
	}
	return []Role{RoleUser}, nil // Default for all registered users
}

// CanAccess checks if a user can access a specific tool
func (r *RBAC) CanAccess(userID, tool string) (bool, error) {
	roles, err := r.UserRoles(userID)
	if err != nil {
		return false, err
	}

	allowed, ok := r.toolRoles[tool]
	if !ok {
		return false, nil // No rule defined → deny by default
	}

	for _, ur := range roles {
		if _, ok := allowed[ur]; ok {
			return true, nil
		}
	}
	return false, nil
}

// DefaultRBAC provides a global singleton instance
var (
	DefaultRBAC = NewRBAC()
	once       sync.Once
)

// GetDefaultRBAC returns the default RBAC instance
func GetDefaultRBAC() *RBAC {
	once.Do(func() {
		DefaultRBAC = NewRBAC()
	})
	return DefaultRBAC
}