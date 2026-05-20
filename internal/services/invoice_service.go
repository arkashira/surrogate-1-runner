package services

import (
	"fmt"
	"log"
	"os"
	"path/filepath"
)

type InvoiceService struct{}

func NewInvoiceService() *InvoiceService {
	return &InvoiceService{}
}

func (is *InvoiceService) StoreInvoiceData(file *os.File) error {
	// Implement logic to store parsed invoice data in persistent storage
	// This could involve writing to a database or another storage mechanism
	log.Printf("Storing invoice data from file: %s", file.Name())
	return nil
}

func ValidateAndStoreFile(filePath string) error {
	file, err := os.Open(filePath)
	if err != nil {
		return fmt.Errorf("failed to open file: %w", err)
	}
	defer file.Close()

	ext := filepath.Ext(filePath)
	switch ext {
	case ".csv":
		// Add CSV validation logic here
	case ".pdf":
		// Add PDF validation logic here
	case ".xml":
		// Add XML validation logic here
	default:
		return fmt.Errorf("unsupported file type: %s", ext)
	}

	invoiceService := NewInvoiceService()
	return invoiceService.StoreInvoiceData(file)
}