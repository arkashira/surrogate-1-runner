package routes

import (
	"encoding/csv"
	"fmt"
	"github.com/gin-gonic/gin"
	"io"
	"log"
	"net/http"
	"os"
	"path/filepath"
	"strings"
)

func SetupInvoiceRoutes(router *gin.Engine) {
	router.POST("/invoice/upload", UploadInvoice)
}

func UploadInvoice(c *gin.Context) {
	file, err := c.FormFile("file")
	if err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Failed to get file"})
		return
	}

	tempFile, err := file.Open()
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to open file"})
		return
	}
	defer tempFile.Close()

	switch filepath.Ext(file.Filename) {
	case ".csv":
		reader := csv.NewReader(tempFile)
		_, err := reader.ReadAll()
		if err != nil && err != io.EOF {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid CSV format"})
			return
		}
	case ".pdf":
		// Add PDF validation logic here
	case ".xml":
		// Add XML validation logic here
	default:
		c.JSON(http.StatusBadRequest, gin.H{"error": "Unsupported file type"})
		return
	}

	// Call service to handle the validated file
	err = HandleValidatedFile(file)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to process file"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "File uploaded successfully"})
}

func HandleValidatedFile(file *multipart.FileHeader) error {
	// Implement logic to handle the validated file and store it in persistent storage
	// This could involve calling a service method to parse and store the data
	log.Printf("Handling validated file: %s", file.Filename)
	return nil
}