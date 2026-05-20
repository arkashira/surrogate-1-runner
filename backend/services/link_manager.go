package services

import (
	"time"
)

type Link struct {
	ID        string
	Status    LinkState
	CreatedAt time.Time
	UpdatedAt time.Time
}

// Global notifier – set this from main().
var GlobalNotifier *WebSocketNotifier

func (l *Link) UpdateStatus(newStatus LinkState) {
	l.Status = newStatus
	l.UpdatedAt = time.Now()

	// Notify all WebSocket clients
	if GlobalNotifier != nil {
		GlobalNotifier.EmitLinkStateChange(l.ID, newStatus)
	}
}