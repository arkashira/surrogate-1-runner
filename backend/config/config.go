package config

import (
	"fmt"
	"os"
)

type Email struct {
	SMTPHost     string
	SMTPPort     string
	SMTPUser     string
	SMTPPass     string
	FromAddress  string
	ToAddress    string
	TemplatePath string
}

func LoadEmailConfig() (*Email, error) {
	env := func(k string) string {
		v := os.Getenv(k)
		if v == "" {
			return ""
		}
		return v
	}

	cfg := &Email{
		SMTPHost:     env("SMTP_HOST"),
		SMTPPort:     env("SMTP_PORT"),
		SMTPUser:     env("SMTP_USER"),
		SMTPPass:     env("SMTP_PASS"),
		FromAddress:  env("EMAIL_FROM"),
		ToAddress:    env("EMAIL_TO"),
		TemplatePath: env("EMAIL_TEMPLATE_PATH"),
	}

	// Basic sanity check – all fields must be present
	if cfg.SMTPHost == "" || cfg.SMTPPort == "" || cfg.SMTPUser == "" ||
		cfg.SMTPPass == "" || cfg.FromAddress == "" || cfg.ToAddress == "" ||
		cfg.TemplatePath == "" {
		return nil, fmt.Errorf("incomplete email configuration")
	}
	return cfg, nil
}