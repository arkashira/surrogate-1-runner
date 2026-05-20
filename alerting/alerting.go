package alerting

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/axentx/surrogate-1/api/signature"
	"github.com/axentx/surrogate-1/db"
	"github.com/axentx/surrogate-1/k8s"
	"github.com/axentx/surrogate-1/cicd"
	"github.com/jmoiron/sqlx"
)

// Alert represents a detected API signature change with detailed information
type Alert struct {
	ID          int64     `db:"id" json:"id"`
	Endpoint    string    `db:"endpoint" json:"endpoint"`
	OldSignature string   `db:"old_signature" json:"old_signature"`
	NewSignature string   `db:"new_signature" json:"new_signature"`
	DetectedAt  time.Time `db:"detected_at" json:"detected_at"`
	Severity    string    `db:"severity" json:"severity"` // Added severity level
}

// AlertManager handles detection, persistence, and notification of alerts
type AlertManager struct {
	db          *db.Database
	k8s         *k8s.Kubernetes
	cicd        *cicd.CICD
	webhookURL  string
	httpClient  *http.Client
	alertQueue  chan *Alert
	shutdownCtx context.Context
	shutdown    context.CancelFunc
}

// NewAlertManager creates a new AlertManager with all dependencies
func NewAlertManager(db *db.Database, k8s *k8s.Kubernetes, cicd *cicd.CICD, webhookURL string) *AlertManager {
	ctx, cancel := context.WithCancel(context.Background())
	return &AlertManager{
		db:          db,
		k8s:         k8s,
		cicd:        cicd,
		webhookURL:  webhookURL,
		httpClient:  &http.Client{Timeout: 10 * time.Second},
		alertQueue:  make(chan *Alert, 100),
		shutdownCtx: ctx,
		shutdown:    cancel,
	}
}

// Start begins the background worker that processes alerts
func (am *AlertManager) Start() {
	go am.worker()
	go am.monitorSignatures()
}

// Stop signals the worker to exit
func (am *AlertManager) Stop() {
	am.shutdown()
}

// monitorSignatures periodically checks for signature changes
func (am *AlertManager) monitorSignatures() {
	ticker := time.NewTicker(5 * time.Minute) // Configurable interval
	defer ticker.Stop()

	for {
		select {
		case <-ticker.C:
			am.detectSignatureChanges()
		case <-am.shutdownCtx.Done():
			return
		}
	}
}

// detectSignatureChanges checks for changes in API signatures
func (am *AlertManager) detectSignatureChanges() {
	signatures, err := am.db.GetAPIRequestSignatures()
	if err != nil {
		log.Printf("Failed to get API request signatures: %v", err)
		return
	}

	for _, sig := range signatures {
		if signature.HasChanged(sig) {
			am.TriggerAlert(sig)
		}
	}
}

// TriggerAlert creates and processes a new alert
func (am *AlertManager) TriggerAlert(sig signature.APIRequestSignature) {
	severity := am.determineSeverity(sig) // Added severity determination
	alert := &Alert{
		Endpoint:     sig.Endpoint,
		OldSignature: sig.OldSignature,
		NewSignature: sig.NewSignature,
		DetectedAt:   time.Now(),
		Severity:     severity,
	}

	select {
	case am.alertQueue <- alert:
	case <-am.shutdownCtx.Done():
		log.Println("Alert manager shutting down, dropping alert")
	}
}

// worker processes alerts from the queue
func (am *AlertManager) worker() {
	for {
		select {
		case alert := <-am.alertQueue:
			// Persist to DB
			if err := am.db.StoreAlert(alert); err != nil {
				log.Printf("Failed to store alert: %v", err)
				continue
			}

			// Send notifications
			am.sendNotifications(alert)

		case <-am.shutdownCtx.Done():
			return
		}
	}
}

// sendNotifications sends alert to all configured channels
func (am *AlertManager) sendNotifications(a *Alert) {
	// Send to Kubernetes
	am.k8s.SendAlert(a.Endpoint, a.Severity, a.DetectedAt)

	// Send to CI/CD
	am.cicd.SendAlert(a.Endpoint, a.Severity, a.DetectedAt)

	// Send webhook if configured
	if am.webhookURL != "" {
		if err := am.sendWebhook(a); err != nil {
			log.Printf("Failed to send webhook: %v", err)
		}
	}
}

// sendWebhook posts the alert to the configured webhook URL
func (am *AlertManager) sendWebhook(a *Alert) error {
	payload, err := json.Marshal(a)
	if err != nil {
		return err
	}

	req, err := http.NewRequest("POST", am.webhookURL, bytes.NewBuffer(payload))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")

	resp, err := am.httpClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 300 {
		return fmt.Errorf("webhook returned status %d", resp.StatusCode)
	}
	return nil
}

// determineSeverity analyzes the signature change to determine severity
func (am *AlertManager) determineSeverity(sig signature.APIRequestSignature) string {
	// Implement your severity logic here
	// Example: Compare parameter counts, response structures, etc.
	return "medium" // Default severity
}