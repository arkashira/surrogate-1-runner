package main

import (
	"log"
	"time"
	"net/http"
	"bytes"
	"encoding/json"
)

type Alert struct {
	Labels map[string]string `json:"labels"`
}

func sendAlert(alert Alert) {
	alerts := []Alert{alert}
	data, err := json.Marshal(alerts)
	if err != nil {
		log.Fatalf("Error marshaling alert: %v", err)
	}

	resp, err := http.Post("http://alertmanager:9093/api/v1/alerts", "application/json", bytes.NewBuffer(data))
	if err != nil {
		log.Fatalf("Error sending alert: %v", err)
	}
	defer resp.Body.Close()
	log.Printf("Alert sent with status: %s", resp.Status)
}

func main() {
	// Simulate alerting based on metrics collected
	alert := Alert{
		Labels: map[string]string{
			"alert": "HighAverageMetric",
			"severity": "critical",
		},
	}

	// Example: Simulate sending an alert every minute
	for {
		sendAlert(alert)
		time.Sleep(1 * time.Minute)
	}
}