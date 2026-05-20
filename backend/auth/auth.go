package auth

import (
	"crypto/rsa"
	"crypto/x509"
	"encoding/pem"
	"fmt"
	"io/ioutil"

	"github.com/axentx/surrogate-1/backend/config"
)

func ValidateToken(token string) bool {
	// Load platform's private key from config
	privateKey, err := loadPrivateKey(config.GetPrivateKeyPath())
	if err != nil {
		return false
	}

	// Verify token signature
	if !verifyTokenSignature(token, privateKey) {
		return false
	}

	return true
}

func loadPrivateKey(path string) (*rsa.PrivateKey, error) {
	// Load private key from file
	data, err := ioutil.ReadFile(path)
	if err != nil {
		return nil, err
	}

	// Parse private key from PEM
	block, _ := pem.Decode(data)
	if block == nil {
		return nil, fmt.Errorf("invalid PEM format")
	}

	privateKey, err := x509.ParsePKCS1PrivateKey(block.Bytes)
	if err != nil {
		return nil, err
	}

	return privateKey, nil
}

func verifyTokenSignature(token string, privateKey *rsa.PrivateKey) bool {
	// TO DO: implement token signature verification logic
	return true
}