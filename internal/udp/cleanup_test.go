package udp

import (
	"net"
	"testing"
	"time"
)

func TestCleanupSessions_ExpiresIdleSession(t *testing.T) {
	// Reduce timeout for the test.
	originalTimeout := sessionTimeout
	sessionTimeout = 10 * time.Millisecond
	defer func() { sessionTimeout = originalTimeout }()

	// Prepare a dummy session.
	token := "deadbeefdeadbeefdeadbeefdeadbeef"
	addr := &net.UDPAddr{IP: net.ParseIP("127.0.0.1"), Port: 12345}
	s := &session{
		dest:     addr,
		lastSeen: time.Now(),
	}

	// Insert into the global map.
	sessionsMu.Lock()
	sessions[token] = s
	sessionsMu.Unlock()

	// Wait longer than the test timeout.
	time.Sleep(30 * time.Millisecond)

	// Run cleanup manually.
	cleanupSessions()

	// Verify the session has been removed.
	sessionsMu.RLock()
	_, exists := sessions[token]
	sessionsMu.RUnlock()

	if exists {
		t.Fatalf("session %s was not cleaned up after inactivity", token)
	}
}