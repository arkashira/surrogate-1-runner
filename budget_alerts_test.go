package main

import (
	"testing"
)

func TestCheckAndSendAlert(t *testing.T) {
	alert := NewBudgetAlert(1000.0, "user@example.com")
	alert.CheckAndSendAlert(1200.0)
	// Add more test cases as needed
}

func TestSendEmailAlert(t *testing.T) {
	alert := NewBudgetAlert(1000.0, "user@example.com")
	alert.sendEmailAlert(1200.0)
	// Add more test cases as needed
}