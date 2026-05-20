package udp

import (
	"log"
	"time"
)

const (
	// defaultSessionTimeout is the inactivity period after which a session is
	// considered expired. It matches the acceptance criteria (5 minutes).
	defaultSessionTimeout = 5 * time.Minute
)

// sessionTimeout can be overridden in tests.
var sessionTimeout = defaultSessionTimeout

// init starts the background goroutine that periodically cleans up stale sessions.
func init() {
	go sessionCleanupWorker()
}

// sessionCleanupWorker runs forever, invoking cleanupSessions at a regular interval.
func sessionCleanupWorker() {
	ticker := time.NewTicker(time.Minute)
	defer ticker.Stop()

	for range ticker.C {
		cleanupSessions()
	}
}

// cleanupSessions removes entries from the global session map that have been idle
// longer than sessionTimeout. It is safe to call from multiple goroutines because
// it acquires the sessions mutex defined in sessions.go.
func cleanupSessions() {
	sessionsMu.Lock()
	defer sessionsMu.Unlock()

	now := time.Now()
	for token, s := range sessions {
		if now.Sub(s.lastSeen) > sessionTimeout {
			delete(sessions, token)
			log.Printf("udp: session %s expired after %s of inactivity", token, sessionTimeout)
		}
	}
}