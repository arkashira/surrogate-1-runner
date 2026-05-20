package service_mapper

import (
	"strings"
	"sync"
)

// UpstreamInfo holds metadata about the upstream service that satisfied a request.
type UpstreamInfo struct {
	ServiceName string // e.g. "UserService"
	Endpoint    string // e.g. "/v1/users/123"
}

// ---------------------------------------------------------------------
// 1️⃣  Prefix‑based static map (fallback when no request‑ID is known)
// ---------------------------------------------------------------------

// staticMap is a read‑only map that matches request‑path prefixes to a service.
// Extend this map whenever a new micro‑service is added.
var staticMap = map[string]UpstreamInfo{
	"/api/user":    {"UserService", "/user"},
	"/api/order":   {"OrderService", "/order"},
	"/api/payment": {"PaymentService", "/payment"},
}

// GetByPath returns the static mapping for a raw HTTP path.
// If no prefix matches, the second return value is false.
func GetByPath(path string) (UpstreamInfo, bool) {
	if !strings.HasPrefix(path, "/") {
		path = "/" + path
	}
	for prefix, info := range staticMap {
		if strings.HasPrefix(path, prefix) {
			// Trim the matched prefix so the endpoint reflects the remainder.
			rem := strings.TrimPrefix(path, prefix)
			if rem == "" {
				rem = "/"
			}
			return UpstreamInfo{
				ServiceName: info.ServiceName,
				Endpoint:    rem,
			}, true
		}
	}
	return UpstreamInfo{}, false
}

// ---------------------------------------------------------------------
// 2️⃣  Dynamic request‑ID → upstream map (thread‑safe)
// ---------------------------------------------------------------------

type dynamicMapper struct {
	m sync.Map // map[string]UpstreamInfo
}

// defaultMapper is the singleton used by the rest of the code base.
var defaultMapper = &dynamicMapper{}

// Set registers upstream metadata for a given request ID.
// Called by the routing layer as soon as it knows which service will handle the request.
func Set(requestID string, info UpstreamInfo) {
	defaultMapper.m.Store(requestID, info)
}

// Get retrieves upstream metadata for a request ID.
// If the ID is unknown, the bool return is false.
func Get(requestID string) (UpstreamInfo, bool) {
	if v, ok := defaultMapper.m.Load(requestID); ok {
		if info, ok := v.(UpstreamInfo); ok {
			return info, true
		}
	}
	return UpstreamInfo{}, false
}

// Delete removes a mapping once the request lifecycle is finished.
func Delete(requestID string) {
	defaultMapper.m.Delete(requestID)
}