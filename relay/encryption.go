package relay

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"errors"
	"fmt"
)

// EncryptPayload encrypts data using the provided public key
// Returns base64 encoded ciphertext or error
func EncryptPayload(publicKeyPEM string, data []byte) ([]byte, error) {
	block, _ := pem.Decode([]byte(publicKeyPEM))
	if block == nil || block.Type != "PUBLIC KEY" {
		return nil, errors.New("invalid public key format")
	}

	pubKey, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		return nil, fmt.Errorf("failed to parse public key: %w", err)
	}

	rsaKey, ok := pubKey.(*rsa.PublicKey)
	if !ok {
		return nil, errors.New("parsed key is not an RSA public key")
	}

	ciphertext, err := rsa.EncryptOAEP(
		rand.Reader,
		nil,
		rsaKey,
		data,
		nil,
	)
	if err != nil {
		return nil, fmt.Errorf("encryption failed: %w", err)
	}

	return ciphertext, nil
}

// DecryptPayload decrypts data using the private key
// For relay internal processing only
func DecryptPayload(privateKey *rsa.PrivateKey, ciphertext []byte) ([]byte, error) {
	plaintext, err := rsa.DecryptOAEP(
		rand.Reader,
		nil,
		privateKey,
		ciphertext,
		nil,
	)
	if err != nil {
		return nil, fmt.Errorf("decryption failed: %w", err)
	}

	return plaintext, nil
}

// ValidatePublicKey checks if the PEM string is a valid RSA public key
func ValidatePublicKey(publicKeyPEM string) error {
	block, _ := pem.Decode([]byte(publicKeyPEM))
	if block == nil || block.Type != "PUBLIC KEY" {
		return errors.New("invalid public key format")
	}

	_, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		return fmt.Errorf("invalid public key: %w", err)
	}

	return nil
}