package services

import (
	"context"
	"crypto/rand"
	"crypto/sha256"
	"encoding/base64"
	"errors"
	"time"

	"github.com/axentx/surrogate-1/models"
	"github.com/axentx/surrogate-1/repositories"
	"github.com/google/uuid"
	"golang.org/x/crypto/pbkdf2"
)

const (
	// TokenConfig holds configuration for recovery tokens
	TokenConfig = struct {
		Length         int
		SaltLength     int
		Iterations     int
		DefaultExpiry  time.Duration
	}{
		Length:        32,
		SaltLength:    16,
		Iterations:    10000,
		DefaultExpiry: 15 * time.Minute,
	}
)

// RecoveryService handles account recovery flows
type RecoveryService struct {
	tokenRepo repositories.RecoveryTokenRepository
	userRepo  repositories.UserRepository
	logger    Logger
}

// Logger interface for dependency injection
type Logger interface {
	Infof(format string, args ...interface{})
	Errorf(format string, args ...interface{})
}

// NewRecoveryService creates a new RecoveryService
func NewRecoveryService(tokenRepo repositories.RecoveryTokenRepository, userRepo repositories.UserRepository, logger Logger) *RecoveryService {
	return &RecoveryService{
		tokenRepo: tokenRepo,
		userRepo:  userRepo,
		logger:    logger,
	}
}

// GenerateRecoveryToken creates a cryptographically secure recovery token
func GenerateRecoveryToken() (*models.RecoveryToken, error) {
	// Generate random salt
	salt := make([]byte, TokenConfig.SaltLength)
	if _, err := rand.Read(salt); err != nil {
		return nil, errors.New("failed to generate salt")
	}

	// Generate random token
	tokenBytes := make([]byte, TokenConfig.Length)
	if _, err := rand.Read(tokenBytes); err != nil {
		return nil, errors.New("failed to generate token")
	}

	token := base64.URLEncoding.EncodeToString(tokenBytes)

	return &models.RecoveryToken{
		Token:     token,
		Salt:      salt,
		ExpiresAt: time.Now().Add(TokenConfig.DefaultExpiry),
	}, nil
}

// HashToken creates a secure hash of the token using PBKDF2
func HashToken(token string, salt []byte) string {
	hash := pbkdf2.Key([]byte(token), salt, TokenConfig.Iterations, TokenConfig.Length, sha256.New)
	return base64.StdEncoding.EncodeToString(hash)
}

// ValidateToken validates a recovery token and returns the associated user
func (s *RecoveryService) ValidateToken(ctx context.Context, token string) (*models.User, error) {
	if token == "" {
		return nil, errors.New("token is required")
	}

	// Fetch token record from storage
	recToken, err := s.tokenRepo.FindByToken(ctx, token)
	if err != nil {
		s.logger.Errorf("token lookup error: %v", err)
		return nil, errors.New("invalid token")
	}
	if recToken == nil {
		return nil, errors.New("token not found")
	}

	// CRITICAL: Verify token hash for security
	if !s.verifyTokenHash(token, recToken) {
		s.logger.Errorf("token hash verification failed for token: %s", token[:8]+"...")
		return nil, errors.New("invalid token")
	}

	// Check expiration
	if time.Now().After(recToken.ExpiresAt) {
		// Optionally invalidate expired token
		_ = s.tokenRepo.Delete(ctx, token)
		return nil, errors.New("token expired")
	}

	// Fetch associated user
	user, err := s.userRepo.FindByID(ctx, recToken.UserID)
	if err != nil {
		s.logger.Errorf("user lookup error: %v", err)
		return nil, errors.New("user not found")
	}
	if user == nil {
		return nil, errors.New("user not found")
	}

	// Log successful validation
	s.logger.Infof("Recovery request validated for user %s (token %s)", user.ID, token[:8]+"...")

	return user, nil
}

// verifyTokenHash verifies the token against stored hash
func (s *RecoveryService) verifyTokenHash(token string, storedToken *models.RecoveryToken) bool {
	computedHash := HashToken(token, storedToken.Salt)
	return computedHash == storedToken.Hash
}

// InitiateRecoveryRequest creates a recovery token for a user
func (s *RecoveryService) InitiateRecoveryRequest(ctx context.Context, userID string) (*models.RecoveryToken, error) {
	if userID == "" {
		return nil, errors.New("user ID is required")
	}

	// Verify user exists
	user, err := s.userRepo.FindByID(ctx, userID)
	if err != nil || user == nil {
		return nil, errors.New("user not found")
	}

	// Generate new token
	token, err := GenerateRecoveryToken()
	if err != nil {
		return nil, err
	}

	// Compute hash for storage (never store raw token)
	token.UserID = userID
	token.Hash = HashToken(token.Token, token.Salt)

	// Store token
	if err := s.tokenRepo.Create(ctx, token); err != nil {
		s.logger.Errorf("failed to store recovery token: %v", err)
		return nil, errors.New("failed to create recovery token")
	}

	s.logger.Infof("Recovery token created for user %s", userID)

	// Return token WITHOUT salt (salt should be in token record only)
	return &models.RecoveryToken{
		ID:        token.ID,
		Token:    token.Token,
		UserID:    token.UserID,
		ExpiresAt: token.ExpiresAt,
	}, nil
}

// InvalidateToken removes a recovery token (after successful password reset)
func (s *RecoveryService) InvalidateToken(ctx context.Context, token string) error {
	if token == "" {
		return errors.New("token is required")
	}

	if err := s.tokenRepo.Delete(ctx, token); err != nil {
		s.logger.Errorf("failed to invalidate token: %v", err)
		return errors.New("failed to invalidate token")
	}

	s.logger.Infof("Recovery token invalidated")
	return nil
}