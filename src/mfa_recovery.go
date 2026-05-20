package main

import (
	"crypto/rand"
	"encoding/hex"
	"errors"
	"log"
	"sync"
	"time"
)

// RecoveryMethod represents the supported MFA recovery channels.
type RecoveryMethod string

const (
	RecoveryMethodSMS        RecoveryMethod = "sms"
	RecoveryMethodEmail      RecoveryMethod = "email"
	RecoveryMethodBackupCode RecoveryMethod = "backup_code"
)

// RecoveryToken holds the data for a single recovery attempt.
type RecoveryToken struct {
	Token     string
	UserID    string
	Method    RecoveryMethod
	ExpiresAt time.Time
}

// RecoveryService manages MFA recovery tokens and audit logging.
type RecoveryService struct {
	mu     sync.Mutex
	tokens map[string]RecoveryToken
}

// NewRecoveryService creates a new in‑memory recovery service.
func NewRecoveryService() *RecoveryService {
	return &RecoveryService{
		tokens: make(map[string]RecoveryToken),
	}
}

// generateToken creates a cryptographically secure random token.
func (s *RecoveryService) generateToken() (string, error) {
	b := make([]byte, 32)
	if _, err := rand.Read(b); err != nil {
		return "", err
	}
	return hex.EncodeToString(b), nil
}

// RequestRecovery initiates a recovery process for a user and method.
// It returns a token that must be sent to the user via the chosen method.
func (s *RecoveryService) RequestRecovery(userID string, method RecoveryMethod) (RecoveryToken, error) {
	tokenStr, err := s.generateToken()
	if err != nil {
		return RecoveryToken{}, err
	}
	token := RecoveryToken{
		Token:     tokenStr,
		UserID:    userID,
		Method:    method,
		ExpiresAt: time.Now().Add(15 * time.Minute),
	}

	s.mu.Lock()
	s.tokens[tokenStr] = token
	s.mu.Unlock()

	// In a real system, send the token via SMS/Email/BackupCode here.
	log.Printf("[Recovery] Generated token for user %s via %s", userID, method)

	return token, nil
}

// VerifyRecoveryToken checks if the provided token is valid and not expired.
// If valid, it returns the associated RecoveryToken and removes it from the store.
func (s *RecoveryService) VerifyRecoveryToken(tokenStr string) (RecoveryToken, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	token, ok := s.tokens[tokenStr]
	if !ok {
		return RecoveryToken{}, errors.New("invalid token")
	}
	if time.Now().After(token.ExpiresAt) {
		delete(s.tokens, tokenStr)
		return RecoveryToken{}, errors.New("token expired")
	}

	// Token is valid; remove it to prevent reuse.
	delete(s.tokens, tokenStr)

	// Log the successful verification for audit.
	log.Printf("[Recovery] Token verified for user %s via %s", token.UserID, token.Method)

	return token, nil
}

// LogRecoveryAction records a recovery action for audit purposes.
// In a real system this would write to a persistent audit log.
func (s *RecoveryService) LogRecoveryAction(userID string, action string) {
	log.Printf("[Recovery] User %s performed action: %s", userID, action)
}