
package compliance

import (
	"bytes"
	"context"
	"crypto/tls"
	"fmt"
	"net/smtp"
	"os"
	"sync"
	"time"

	"github.com/axentx/surrogate-1-runner/config"
	"github.com/axentx/surrogate-1-runner/logger"
)

// EmailNotifier handles email notifications for compliance violations
type EmailNotifier struct {
	mu          sync.Mutex
	lastAlerts  map[string]time.Time
	throttleDur time.Duration
}

// NewEmailNotifier creates a new email notifier with throttling
func NewEmailNotifier() *EmailNotifier {
	cfg := config.GetConfig()
	return &EmailNotifier{
		lastAlerts:  make(map[string]time.Time),
		throttleDur: time.Duration(cfg.Email.ThrottleMinutes) * time.Minute,
	}
}

// SendAlert sends an email notification for a compliance violation
func (e *EmailNotifier) SendAlert(ctx context.Context, policyName string, violationDetails string) error {
	cfg := config.GetConfig()
	emailConfig := cfg.Email
	
	// Check if we should throttle this alert
	if !e.canSendAlert(policyName) {
		logger.Debug(ctx, fmt.Sprintf("Throttling alert for policy %s", policyName))
		return nil
	}
	
	// Prepare email content
	subject := fmt.Sprintf("Compliance Violation Alert: %s", policyName)
	body := fmt.Sprintf(
		"Policy Name: %s\n"+
		"Timestamp: %s\n"+
		"Violation Details:\n%s\n"+
		"System: Surrogate-1\n",
		policyName,
		time.Now().Format(time.RFC3339),
		violationDetails,
	)
	
	// Create message
	message := bytes.NewBufferString(
		fmt.Sprintf("From: %s\r\n"+
			"To: %s\r\n"+
			"Subject: %s\r\n"+
			"Content-Type: text/plain; charset=UTF-8\r\n"+
			"\r\n"+
			"%s",
			emailConfig.From,
			emailConfig.To,
			subject,
			body,
		),
	)
	
	// Configure TLS
	tlsConfig := &tls.Config{
		ServerName: emailConfig.Host,
	}
	
	// Connect to SMTP server
	conn, err := tls.Dial("tcp", fmt.Sprintf("%s:%d", emailConfig.Host, emailConfig.Port), tlsConfig)
	if err != nil {
		logger.Error(ctx, fmt.Sprintf("Failed to connect to SMTP server: %v", err))
		return err
	}
	defer conn.Close()
	
	// Create SMTP client
	client, err := smtp.NewClient(conn, emailConfig.Host)
	if err != nil {
		logger.Error(ctx, fmt.Sprintf("Failed to create SMTP client: %v", err))
		return err
	}
	defer client.Quit()
	
	// Authenticate
	auth := smtp.PlainAuth("", emailConfig.Username, emailConfig.Password, emailConfig.Host)
	if err = client.Auth(auth); err != nil {
		logger.Error(ctx, fmt.Sprintf("SMTP authentication failed: %v", err))
		return err
	}
	
	// Set sender and recipient
	if err = client.Mail(emailConfig.From); err != nil {
		logger.Error(ctx, fmt.Sprintf("SMTP MAIL command failed: %v", err))
		return err
	}
	
	toAddresses := []string{emailConfig.To}
	for _, addr := range toAddresses {
		if err = client.Rcpt(addr); err != nil {
			logger.Error(ctx, fmt.Sprintf("SMTP RCPT command failed for %s: %v", addr, err))
			return err
		}
	}
	
	// Send the email
	writer, err := client.Data()
	if err != nil {
		logger.Error(ctx, fmt.Sprintf("SMTP DATA command failed: %v", err))
		return err
	}
	
	_, err = writer.Write(message.Bytes())
	if err != nil {
		logger.Error(ctx, fmt.Sprintf("Failed to write email data: %v", err))
		return err
	}
	
	err = writer.Close()
	if err != nil {
		logger.Error(ctx, fmt.Sprintf("Failed to close email writer: %v", err))
		return err
	}
	
	// Record successful alert
	e.recordAlert(policyName)
	
	logger.Info(ctx, fmt.Sprintf("Successfully sent email alert for policy %s", policyName))
	return nil
}

// canSendAlert checks if an alert can be sent based on throttling rules
func (e *EmailNotifier) canSendAlert(policyName string) bool {
	e.mu.Lock()
	defer e.mu.Unlock()
	
	lastAlert, exists := e.lastAlerts[policyName]
	
	// If no previous alert or enough time has passed, allow sending
	if !exists || time.Since(lastAlert) >= e.throttleDur {
		return true
	}
	
	// Otherwise, throttle
	return false
}

// recordAlert records when an alert was sent
func (e *EmailNotifier) recordAlert(policyName string) {
	e.mu.Lock()
	defer e.mu.Unlock()
	
	e.lastAlerts[policyName] = time.Now()
}

// LogAlert logs a compliance violation to audit trail
func LogAlert(ctx context.Context, policyName string, violationDetails string) error {
	cfg := config.GetConfig()
	
	// Open audit trail file
	file, err := os.OpenFile(cfg.Audit.TrailPath, os.O_APPEND|os.O_CREATE|os.O_WRONLY, 0644)
	if err != nil {
		logger.Error(ctx, fmt.Sprintf("Failed to open audit trail file: %v", err))
		return err
	}
	defer file.Close()
	
	// Format audit entry
	entry := fmt.Sprintf(
		"[%s] Policy: %s | Details: %s\n",
		time.Now().Format(time.RFC3339),
		policyName,
		violationDetails,
	)
	
	// Write to file
	_, err = file.WriteString(entry)
	if err != nil {
		logger.Error(ctx, fmt.Sprintf("Failed to write to audit trail: %v", err))
		return err
	}
	
	logger.Info(ctx, fmt.Sprintf("Logged alert to audit trail for policy %s", policyName))
	return nil
}

// AlertSystem manages the complete compliance alert workflow
type AlertSystem struct {
	emailNotifier *EmailNotifier
}

// NewAlertSystem creates a new alert system
func NewAlertSystem() *AlertSystem {
	return &AlertSystem{
		emailNotifier: NewEmailNotifier(),
	}
}

// ProcessViolation processes a compliance violation and triggers alerts
func (as *AlertSystem) ProcessViolation(ctx context.Context, policyName string, violationDetails string) error {
	// Log to audit trail first
	if err := LogAlert(ctx, policyName, violationDetails); err != nil {
		return fmt.Errorf("failed to log to audit trail: %w", err)
	}
	
	// Send email alert
	if err := as.emailNotifier.SendAlert(ctx, policyName, violationDetails); err != nil {
		return fmt.Errorf("failed to send email alert: %w", err)
	}
	
	return nil
}