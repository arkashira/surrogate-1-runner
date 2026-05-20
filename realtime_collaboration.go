package main

import (
	"fmt"
	"sync"
)

type TerminalSession struct {
	users     map[string]bool
	mu        sync.RWMutex
	updatesCh chan string
}

func NewTerminalSession() *TerminalSession {
	return &TerminalSession{
		users:     make(map[string]bool),
		updatesCh: make(chan string),
	}
}

func (ts *TerminalSession) Join(user string) {
	ts.mu.Lock()
	defer ts.mu.Unlock()
	ts.users[user] = true
	fmt.Printf("User %s joined the session.\n", user)
}

func (ts *TerminalSession) Leave(user string) {
	ts.mu.Lock()
	defer ts.mu.Unlock()
	delete(ts.users, user)
	fmt.Printf("User %s left the session.\n", user)
}

func (ts *TerminalSession) BroadcastUpdate(update string) {
	ts.updatesCh <- update
}

func (ts *TerminalSession) StartRealtimeUpdates() {
	go func() {
		for update := range ts.updatesCh {
			ts.mu.RLock()
			for user := range ts.users {
				fmt.Printf("Sending update to %s: %s\n", user, update)
			}
			ts.mu.RUnlock()
		}
	}()
}

func main() {
	session := NewTerminalSession()
	session.Join("user1")
	session.Join("user2")

	session.StartRealtimeUpdates()

	session.BroadcastUpdate("Hello, everyone!")
}