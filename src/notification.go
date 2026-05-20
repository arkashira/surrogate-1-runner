package notification

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/smtp"
	"os"

	"github.com/axentx/surrogate-1/config"
)

func sendSlackNotification(eventType string, payload interface{}) error {
	webhookURL := config.GetSlackWebhookURL()
	payloadBytes, err := json.Marshal(payload)
	if err != nil {
		return err
	}

	req, err := http.NewRequest(http.MethodPost, webhookURL, bytes.NewBuffer(payloadBytes))
	if err != nil {
		return err
	}

	req.Header.Set("Content-Type", "application/json")
	client := &http.Client{}
	_, err = client.Do(req)
	if err != nil {
		return err
	}

	return nil
}

func sendEmailNotification(eventType string, to string, body string) error {
	smtpServer := config.GetSMTPServer()
	auth := smtp.PlainAuth("", config.GetSMTPUsername(), config.GetSMTPPassword(), smtpServer.Host)

	msg := []byte("To: " + to + "\r\n" +
		"Subject: Axentx Notification - " + eventType + "\r\n" +
		"\r\n" +
		body + "\r\n")

	err := smtp.SendMail(smtpServer.Addr, auth, config.GetSMTPFrom(), []string{to}, msg)
	if err != nil {
		return err
	}

	return nil
}