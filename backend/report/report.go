package report

import (
	"encoding/json"
	"fmt"
	"log"
	"time"

	"github.com/axentx/surrogate-1/backend/config"
)

func Generate(month string) ([]byte, error) {
	// TO DO: implement report generation logic
	return nil, nil
}

func SignReport(reportData []byte) ([]byte, error) {
	// Load platform's private key from config
	privateKeyPath := config.GetPrivateKeyPath()
	privateKey, err := loadPrivateKey(privateKeyPath)
	if err != nil {
		return nil, err
	}

	// Sign report with private key
	signedReport, err := signReport(reportData, privateKey)
	if err != nil {
		return nil, err
	}

	return signedReport, nil
}

func loadPrivateKey(path string) (*rsa.PrivateKey, error) {
	// TO DO: implement private key loading logic
	return nil, nil
}

func signReport(reportData []byte, privateKey *rsa.PrivateKey) ([]byte, error) {
	// TO DO: implement report signing logic
	return nil, nil
}