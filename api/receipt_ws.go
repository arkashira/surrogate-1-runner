package api

import (
	"encoding/json"
	"errors"
	"net/http"
	"os"
	"strings"
	"sync"

	"github.com/golang-jwt/jwt/v4"
	"github.com/gorilla/websocket"
)

// Receipt represents the data sent to the client after a trade execution.
type Receipt struct {
	TxHash      string `json:"tx_hash"`
	BlockNumber uint64 `json:"block_number"`
	GasUsed     uint64 `json:"gas_used"`
}

// wsManager holds active WebSocket connections grouped by session token.
type wsManager struct {
	mu          sync.RWMutex
	connections map[string]map[*websocket.Conn]struct{}
}

var manager = &wsManager{
	connections: make(map[string]map[*websocket.Conn]struct{}),
}

// add registers a new connection under the given session token.
func (m *wsManager) add(session string, conn *websocket.Conn) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if _, ok := m.connections[session]; !ok {
		m.connections[session] = make(map[*websocket.Conn]struct{})
	}
	m.connections[session][conn] = struct{}{}
}

// remove unregisters a connection.
func (m *wsManager) remove(session string, conn *websocket.Conn) {
	m.mu.Lock()
	defer m.mu.Unlock()
	if conns, ok := m.connections[session]; ok {
		delete(conns, conn)
		if len(conns) == 0 {
			delete(m.connections, session)
		}
	}
}

// broadcast sends a receipt to all connections subscribed to the session.
func (m *wsManager) broadcast(session string, receipt Receipt) error {
	m.mu.RLock()
	conns, ok := m.connections[session]
	m.mu.RUnlock()
	if !ok {
		return errors.New("no subscribers for session")
	}

	payload, err := json.Marshal(receipt)
	if err != nil {
		return err
	}

	for conn := range conns {
		if err := conn.WriteMessage(websocket.TextMessage, payload); err != nil {
			// On write error, clean up the connection.
			m.remove(session, conn)
			_ = conn.Close()
		}
	}
	return nil
}

// BroadcastReceipt is the public API used by other parts of the system to push a receipt.
func BroadcastReceipt(session string, receipt Receipt) error {
	return manager.broadcast(session, receipt)
}

// jwtClaims defines the expected JWT payload.
type jwtClaims struct {
	Session string `json:"session"`
	jwt.RegisteredClaims
}

// getJWTSecret fetches the HMAC secret used to sign JWTs.
func getJWTSecret() []byte {
	secret := os.Getenv("JWT_SECRET")
	if secret == "" {
		// Fallback to a hard‑coded development secret; in production this env must be set.
		secret = "dev-secret"
	}
	return []byte(secret)
}

// validateToken parses and validates the JWT, returning the session token.
func validateToken(tokenString string) (string, error) {
	claims := &jwtClaims{}
	_, err := jwt.ParseWithClaims(tokenString, claims, func(t *jwt.Token) (interface{}, error) {
		// Ensure token is signed with HMAC.
		if _, ok := t.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, errors.New("unexpected signing method")
		}
		return getJWTSecret(), nil
	})
	if err != nil {
		return "", err
	}
	if claims.Session == "" {
		return "", errors.New("session claim missing")
	}
	return claims.Session, nil
}

// upgrader is configured for the WebSocket handshake.
var upgrader = websocket.Upgrader{
	CheckOrigin: func(r *http.Request) bool {
		// Allow any origin; authentication is handled via JWT.
		return true
	},
}

// ReceiptWSHandler upgrades the HTTP request to a WebSocket, authenticates the client,
// and registers the connection for receipt pushes.
func ReceiptWSHandler(w http.ResponseWriter, r *http.Request) {
	// Expect the JWT in the "token" query parameter.
	rawToken := r.URL.Query().Get("token")
	if rawToken == "" {
		http.Error(w, "missing token query parameter", http.StatusUnauthorized)
		return
	}
	// Tokens may be prefixed with "Bearer ".
	if strings.HasPrefix(strings.ToLower(rawToken), "bearer ") {
		rawToken = strings.TrimSpace(rawToken[7:])
	}

	session, err := validateToken(rawToken)
	if err != nil {
		http.Error(w, "invalid token: "+err.Error(), http.StatusUnauthorized)
		return
	}

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		// Upgrade already wrote the error response.
		return
	}
	// Register the connection.
	manager.add(session, conn)

	// Listen for close messages to clean up.
	go func() {
		defer func() {
			manager.remove(session, conn)
			_ = conn.Close()
		}()
		for {
			// We don't expect any inbound messages; just read to detect closure.
			if _, _, err := conn.NextReader(); err != nil {
				return
			}
		}
	}()
}