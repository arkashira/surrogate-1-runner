
package models

import (
	"time"

	"github.com/ethereum/go-ethereum/accounts/keystore"
)

type User struct {
	ID       int64     `json:"id"`
	Account  keystore.Key `json:"account"`
	SessionToken []byte `json:"session_token"`
	LastActivity time.Time `json:"last_activity"`
}

func (u *User) SetSessionToken(token []byte) {
	u.SessionToken = token
	u.LastActivity = time.Now()
}

func (u *User) CheckSessionToken(token []byte) bool {
	// Decrypt session_token and compare with b'session_token'
	// Return true if they match, false otherwise
}