package config

import (
	"crypto/tls"
	"encoding/json"
	"errors"
	"fmt"
	"net/http"
	"time"

	"golang.org/x/crypto/bcrypt"
)

type Config struct {
	PrometheusURL     string `json:"prometheus_url"`
	GrafanaAPIKey     string `json:"grafana_api_key"`
	OTELCollectorURL  string `json:"otel_collector_url"`
}

func ValidateConfig(cfg *Config) error {
	if err := validatePrometheusURL(cfg.PrometheusURL); err != nil {
		return fmt.Errorf("prometheus url validation failed: %w", err)
	}
	if err := validateGrafanaAPIKey(cfg.GrafanaAPIKey); err != nil {
		return fmt.Errorf("grafana api key validation failed: %w", err)
	}
	if err := validateOTELCollectorURL(cfg.OTELCollectorURL); err != nil {
		return fmt.Errorf("otel collector url validation failed: %w", err)
	}
	return nil
}

func validatePrometheusURL(url string) error {
	client := &http.Client{
		Timeout: time.Second * 10,
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		},
	}
	resp, err := client.Get(url + "/api/v1/query")
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return errors.New("invalid prometheus url")
	}
	return nil
}

func validateGrafanaAPIKey(apiKey string) error {
	hashedKey, err := bcrypt.GenerateFromPassword([]byte(apiKey), bcrypt.DefaultCost)
	if err != nil {
		return err
	}
	if len(hashedKey) == 0 {
		return errors.New("invalid grafana api key")
	}
	return nil
}

func validateOTELCollectorURL(url string) error {
	client := &http.Client{
		Timeout: time.Second * 10,
		Transport: &http.Transport{
			TLSClientConfig: &tls.Config{InsecureSkipVerify: true},
		},
	}
	resp, err := client.Post(url, "application/json", nil)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusAccepted {
		return errors.New("invalid otel collector url")
	}
	return nil
}