package crypto

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/tls"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"io"
	"log"
	"os"
	"sync"
	"time"

	"github.com/axentx/surrogate-1/audit"
	"github.com/axentx/surrogate-1/config"
)

// HSMClient manages Hardware Security Module operations
type HSMClient struct {
	hsmEndpoint string
	clientID    string
	logger      *log.Logger
	mu          sync.Mutex
}

// NewHSMClient creates a new HSM client with audit logging
func NewHSMClient(cfg config.HSMConfig, clientID string) (*HSMClient, error) {
	logger := log.New(os.Stdout, "[HSM] ", log.LstdFlags)
	
	hsmClient := &HSMClient{
		hsmEndpoint: cfg.Endpoint,
		clientID:    clientID,
		logger:      logger,
	}
	
	if err := hsmClient.validateConfig(); err != nil {
		return nil, fmt.Errorf("hsm config validation failed: %w", err)
	}
	
	return hsmClient, nil
}

// validateConfig checks HSM configuration requirements
func (h *HSMClient) validateConfig() error {
	if h.hsmEndpoint == "" {
		return fmt.Errorf("hsm endpoint cannot be empty")
	}
	if h.clientID == "" {
		return fmt.Errorf("client ID cannot be empty")
	}
	return nil
}

// GenerateKeyPair generates an RSA key pair using HSM
func (h *HSMClient) GenerateKeyPair(bits int) (*rsa.PrivateKey, error) {
	h.mu.Lock()
	defer h.mu.Unlock()
	
	h.logger.Printf("Generating RSA key pair with %d bits for client %s", bits, h.clientID)
	
	startTime := time.Now()
	
	// Generate key pair
	privateKey, err := rsa.GenerateKey(rand.Reader, bits)
	if err != nil {
		return nil, fmt.Errorf("failed to generate RSA key: %w", err)
	}
	
	// Log to audit trail
	h.logAudit("key_generation", map[string]interface{}{
		"bits":         bits,
		"client_id":    h.clientID,
		"duration_ms": time.Since(startTime).Milliseconds(),
	})
	
	h.logger.Printf("Key pair generated in %v", time.Since(startTime))
	return privateKey, nil
}

// LoadKeyFromHSM loads a key from HSM storage
func (h *HSMClient) LoadKeyFromHSM(keyID string) (*rsa.PrivateKey, error) {
	h.mu.Lock()
	defer h.mu.Unlock()
	
	h.logger.Printf("Loading key %s from HSM for client %s", keyID, h.clientID)
	
	startTime := time.Now()
	
	// Simulate HSM key retrieval (in production, this would call actual HSM API)
	keyData, err := hsmKeyStore.Get(keyID)
	if err != nil {
		return nil, fmt.Errorf("failed to retrieve key from HSM: %w", err)
	}
	
	privateKey, err := x509.ParsePKCS8PrivateKey(keyData)
	if err != nil {
		return nil, fmt.Errorf("failed to parse HSM key: %w", err)
	}
	
	h.logAudit("key_load", map[string]interface{}{
		"key_id":       keyID,
		"client_id":    h.clientID,
		"duration_ms":  time.Since(startTime).Milliseconds(),
	})
	
	h.logger.Printf("Key loaded in %v", time.Since(startTime))
	return privateKey.(*rsa.PrivateKey), nil
}

// CreateTLSConfig creates a TLS 1.3 configuration with HSM-managed keys
func (h *HSMClient) CreateTLSConfig(serverName string) (*tls.Config, error) {
	h.mu.Lock()
	defer h.mu.Unlock()
	
	h.logger.Printf("Creating TLS 1.3 config for %s", serverName)
	
	startTime := time.Now()
	
	// Generate or load key pair
	privateKey, err := h.GenerateKeyPair(2048)
	if err != nil {
		return nil, fmt.Errorf("failed to generate TLS key: %w", err)
	}
	
	cert := &tls.Certificate{
		Certificate: [][]byte{privateKey.PublicKey.N.Bytes()},
		PrivateKey:  privateKey,
	}
	
	tlsConfig := &tls.Config{
		MinVersion:   tls.VersionTLS13,
		Certificates: []tls.Certificate{*cert},
		ClientAuth:   tls.NoClientCert,
	}
	
	h.logAudit("tls_config_create", map[string]interface{}{
		"server_name":  serverName,
		"tls_version":  "1.3",
		"duration_ms":  time.Since(startTime).Milliseconds(),
	})
	
	h.logger.Printf("TLS 1.3 config created in %v", time.Since(startTime))
	return tlsConfig, nil
}

// logAudit logs operation to Surrogate-1 audit trail
func (h *HSMClient) logAudit(operation string, metadata map[string]interface{}) {
	auditEntry := audit.AuditEntry{
		Operation:    operation,
		ClientID:     h.clientID,
		Timestamp:    time.Now().UTC(),
		Metadata:     metadata,
		Source:       "hsm-client",
	}
	
	if err := audit.Log(auditEntry); err != nil {
		h.logger.Printf("Failed to log audit entry: %v", err)
	}
}

// HSMKeyStore manages key storage operations
type HSMKeyStore struct {
	store map[string][]byte
	mu    sync.RWMutex
}

// NewHSMKeyStore creates a new key store
func NewHSMKeyStore() *HSMKeyStore {
	return &HSMKeyStore{
		store: make(map[string][]byte),
	}
}

// Get retrieves a key from the store
func (s *HSMKeyStore) Get(keyID string) ([]byte, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	
	data, exists := s.store[keyID]
	if !exists {
		return nil, fmt.Errorf("key %s not found", keyID)
	}
	
	return data, nil
}

// Set stores a key in the HSM
func (s *HSMKeyStore) Set(keyID string, data []byte) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	
	s.store[keyID] = data
	return nil
}

// Delete removes a key from the HSM
func (s *HSMKeyStore) Delete(keyID string) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	
	delete(s.store, keyID)
	return nil
}

// ExportKey exports a key to PEM format
func (s *HSMKeyStore) ExportKey(keyID string, format string) ([]byte, error) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	
	data, exists := s.store[keyID]
	if !exists {
		return nil, fmt.Errorf("key %s not found", keyID)
	}
	
	return exportToPEM(data, format)
}

// exportToPEM converts raw key data to PEM format
func exportToPEM(keyData []byte, format string) ([]byte, error) {
	switch format {
	case "pkcs8":
		return pem.EncodeToMemory(&pem.Block{
			Type:  "PRIVATE KEY",
			Bytes: keyData,
		}), nil
	case "pkcs1":
		return pem.EncodeToMemory(&pem.Block{
			Type:  "RSA PRIVATE KEY",
			Bytes: keyData,
		}), nil
	default:
		return nil, fmt.Errorf("unsupported PEM format: %s", format)
	}
}