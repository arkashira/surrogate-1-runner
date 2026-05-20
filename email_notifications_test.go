package main

import (
	"testing"
)

func TestEmailNotification(t *testing.T) {
	cfg := EmailConfig{
		SMTPHost:    "smtp.example.com",
		SMTPPort:    587,
		Username:    "user@example.com",
		Password:    "testpass123",
		FromAddress: "budget@example.com",
	}

	err := SendBudgetAlertEmail(cfg, "admin@example.com", "Budget Alert", "Test message")
	if err != nil {
		t.Fatalf("Failed to send test email: %v", err)
	}
}