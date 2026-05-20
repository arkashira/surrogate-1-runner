package main

import (
	"golang.org/x/net/smtp"
	"strings"
)

type EmailConfig struct {
	SMTPHost     string
	SMTPPort     int
	Username     string
	Password     string
	FromAddress  string
}

func SendBudgetAlertEmail(cfg EmailConfig, to, subject, body string) error {
	auth := smtp.PlainAuth("", cfg.Username, cfg.Password, cfg.SMTPHost)
	msg := []byte("To: " + to + "\r\n" +
		"Subject: " + subject + "\r\n" +
		"\r\n" +
		body + "\r\n")

	addr := cfg.SMTPHost + ":" + string(cfg.SMTPPort)
	return smtp.SendMail(addr, auth, cfg.FromAddress, []string{to}, msg)
}

func FormatBudgetAlertMessage(threshold, actual float64, currency string) string {
	return strings.TrimSpace(`
Budget threshold exceeded!

Threshold: ` + currency + threshold + `
Actual:    ` + currency + actual + `

Please review your current budget allocation.
`)
}