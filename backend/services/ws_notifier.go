package services

import (
	"encoding/json"
	"log"
	"net/http"
	"sync"

	"github.com/gorilla/websocket"
)

// LinkState is the set of possible states for an approval link.
type LinkState string

const (
	StateActive  LinkState = "active"
	StateUsed    LinkState = "used"
	StateExpired LinkState = "expired"
	StateRevoked LinkState = "revoked"
)

// linkStateChangePayload is the JSON structure that the client receives.
type linkStateChangePayload struct {
	Type      string    `json:"type"`      // always "link_state_change"
	LinkID    string    `json:"link_id"`
	NewState  LinkState `json:"new_state"`
}

// WebSocketNotifier implements a simple pub/sub system for link state changes.
type WebSocketNotifier struct {
	// Map of active connections.
	clients map[*websocket.Conn]bool
	mu      sync.Mutex

	// Upgrader used to upgrade HTTP connections.
	upgrader websocket.Upgrader

	// Buffered channel used for broadcasting events.
	broadcast chan []byte
}

// NewWebSocketNotifier creates a ready‑to‑use notifier.
func NewWebSocketNotifier() *WebSocketNotifier {
	return &WebSocketNotifier{
		clients: make(map[*websocket.Conn]bool),
		upgrader: websocket.Upgrader{
			ReadBufferSize:  1024,
			WriteBufferSize: 1024,
			// In production tighten this to a whitelist of origins.
			CheckOrigin: func(r *http.Request) bool { return true },
		},
		broadcast: make(chan []byte, 256), // 256 queued messages
	}
}

// ServeHTTP upgrades the HTTP connection to a WebSocket and registers the client.
func (n *WebSocketNotifier) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	conn, err := n.upgrader.Upgrade(w, r, nil)
	if err != nil {
		log.Printf("ws upgrade error: %v", err)
		return
	}

	// Register client
	n.mu.Lock()
	n.clients[conn] = true
	n.mu.Unlock()

	// Read loop – only used to detect when the client disconnects.
	go func() {
		defer func() {
			n.mu.Lock()
			delete(n.clients, conn)
			n.mu.Unlock()
			conn.Close()
		}()
		for {
			if _, _, err := conn.NextReader(); err != nil {
				return // client disconnected or error
			}
		}
	}()
}

// Start runs the broadcast loop.  Call this in a goroutine.
func (n *WebSocketNotifier) Start() {
	for msg := range n.broadcast {
		n.mu.Lock()
		for client := range n.clients {
			if err := client.WriteMessage(websocket.TextMessage, msg); err != nil {
				log.Printf("ws write error: %v", err)
				client.Close()
				delete(n.clients, client)
			}
		}
		n.mu.Unlock()
	}
}

// EmitLinkStateChange sends a link‑state‑change event to all connected clients.
// The call is non‑blocking – if the broadcast channel is full the event is dropped.
func (n *WebSocketNotifier) EmitLinkStateChange(linkID string, newState LinkState) {
	payload := linkStateChangePayload{
		Type:     "link_state_change",
		LinkID:   linkID,
		NewState: newState,
	}
	data, err := json.Marshal(payload)
	if err != nil {
		log.Printf("failed to marshal link state change: %v", err)
		return
	}

	select {
	case n.broadcast <- data:
	default:
		log.Printf("broadcast channel full – dropping link state change for %s", linkID)
	}
}