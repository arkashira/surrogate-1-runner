package udp

import (
	"context"
	"fmt"
	"net"
	"sync"
	"time"

	"github.com/pkg/errors"
)

type Session struct {
	Token     [16]byte
	TargetIP  string
	TargetPort int
	LastSeen   time.Time
}

type SessionMap struct {
	sync.RWMutex
	sessions map[[16]byte]*Session
}

func NewSessionMap() *SessionMap {
	return &SessionMap{
		sessions: make(map[[16]byte]*Session),
	}
}

func (sm *SessionMap) AddSession(token [16]byte, targetIP string, targetPort int) {
	sm.Lock()
	defer sm.Unlock()

	sm.sessions[token] = &Session{
		Token:     token,
		TargetIP:  targetIP,
		TargetPort: targetPort,
		LastSeen:   time.Now(),
	}
}

func (sm *SessionMap) GetSession(token [16]byte) (*Session, bool) {
	sm.RLock()
	defer sm.RUnlock()

	session, exists := sm.sessions[token]
	if exists {
		session.LastSeen = time.Now()
	}
	return session, exists
}

func (sm *SessionMap) CleanupExpiredSessions() {
	go func() {
		for {
			time.Sleep(5 * time.Minute)
			sm.Lock()
			for token, session := range sm.sessions {
				if time.Since(session.LastSeen) > 5*time.Minute {
					delete(sm.sessions, token)
				}
			}
			sm.Unlock()
		}
	}()
}

type Listener struct {
	port        int
	sessionMap  *SessionMap
	conn        *net.UDPConn
	ctx         context.Context
	cancelFunc  context.CancelFunc
}

func NewListener(port int) (*Listener, error) {
	l := &Listener{
		port:      port,
		sessionMap: NewSessionMap(),
	}

	l.ctx, l.cancelFunc = context.WithCancel(context.Background())

	addr := fmt.Sprintf(":%d", port)
	conn, err := net.ListenUDP("udp", &net.UDPAddr{Port: port})
	if err != nil {
		return nil, errors.Wrap(err, "failed to listen on UDP port")
	}
	l.conn = conn

	go l.handlePackets()

	return l, nil
}

func (l *Listener) handlePackets() {
	buffer := make([]byte, 1500)
	for {
		n, addr, err := l.conn.ReadFromUDP(buffer)
		if err != nil {
			fmt.Println("Error reading from UDP:", err)
			continue
		}

		token := [16]byte{}
		copy(token[:], buffer[:16])

		session, exists := l.sessionMap.GetSession(token)
		if !exists {
			// Assume the first 16 bytes are the session token
			targetIP := "internal-game-instance-ip" // Replace with actual logic to determine target IP
			targetPort := 5000                      // Replace with actual logic to determine target port
			l.sessionMap.AddSession(token, targetIP, targetPort)
			session, _ = l.sessionMap.GetSession(token)
		}

		// Forward the packet to the internal game instance
		targetAddr := &net.UDPAddr{
			IP:   net.ParseIP(session.TargetIP),
			Port: session.TargetPort,
		}
		_, err = l.conn.WriteToUDP(buffer[:n], targetAddr)
		if err != nil {
			fmt.Println("Error forwarding packet:", err)
		}
	}
}

func (l *Listener) Close() {
	l.cancelFunc()
	l.conn.Close()
}