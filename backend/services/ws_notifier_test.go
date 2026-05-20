package services

import (
	"encoding/json"
	"testing"
	"time"
)

func TestEmitLinkStateChange(t *testing.T) {
	notifier := NewWebSocketNotifier()
	// Use a dummy client to capture the broadcast
	conn, _, err := websocket.DefaultDialer.Dial("ws://localhost:8080/ws/links", nil)
	if err != nil {
		t.Fatalf("dial error: %v", err)
	}
	defer conn.Close()

	// Start notifier in a goroutine
	go notifier.Start()
	// Register the dummy client
	notifier.mu.Lock()
	notifier.clients[conn] = true
	notifier.mu.Unlock()

	// Emit an event
	notifier.EmitLinkStateChange("abc123", StateRevoked)

	// Read the message
	_, msg, err := conn.ReadMessage()
	if err != nil {
		t.Fatalf("read error: %v", err)
	}

	var payload linkStateChangePayload
	if err := json.Unmarshal(msg, &payload); err != nil {
		t.Fatalf("unmarshal error: %v", err)
	}

	if payload.LinkID != "abc123" || payload.NewState != StateRevoked {
		t.Errorf("unexpected payload: %+v", payload)
	}
}