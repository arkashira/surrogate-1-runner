package relay

import (
	"crypto/rand"
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"testing"
)

func generateTestKeyPair() (*rsa.PrivateKey, error) {
	return rsa.GenerateKey(rand.Reader, 2048)
}

func createPEMBlock(key interface{}) string {
	block := &pem.Block{
		Type:  "PUBLIC KEY",
		Bytes: x509.MarshalPKIXPublicKey(key),
	}
	return string(pem.EncodeToMemory(block))
}

func TestEncryptDecrypt(t *testing.T) {
	privKey, err := generateTestKeyPair()
	if err != nil {
		t.Fatal("Failed to generate test key:", err)
	}

	pubPEM := createPEMBlock(&privKey.PublicKey)
	originalData := []byte("signed_transaction_data_123")

	// Test encryption
	encrypted, err := EncryptPayload(pubPEM, originalData)
	if err != nil {
		t.Error("Encryption failed:", err)
	}

	// Test decryption
	decrypted, err := DecryptPayload(privKey, encrypted)
	if err != nil {
		t.Error("Decryption failed:", err)
	}

	if string(decrypted) != string(originalData) {
		t.Error("Data mismatch after encryption/decryption")
	}
}

func TestInvalidKeyValidation(t *testing.T) {
	badKeyPEM := "-----BEGIN PUBLIC KEY-----\ninvalid_key_data\n-----END PUBLIC KEY-----"
	err := ValidatePublicKey(badKeyPEM)
	if err == nil {
		t.Error("Invalid key validation passed unexpectedly")
	}
}