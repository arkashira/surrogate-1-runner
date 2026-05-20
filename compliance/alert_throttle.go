package compliance

import (
	"sync"
	"time"
)

type AlertThrottle struct {
	mu          sync.Mutex
	policyAlert map[string]time.Time
}

func NewAlertThrottle() *AlertThrottle {
	return &AlertThrottle{
		policyAlert: make(map[string]time.Time),
	}
}

func (at *AlertThrottle) ShouldAlert(policyName string) bool {
	at.mu.Lock()
	defer at.mu.Unlock()

	now := time.Now()
	lastAlertTime, exists := at.policyAlert[policyName]

	if !exists {
		at.policyAlert[policyName] = now
		return true
	}

	if now.Sub(lastAlertTime) >= 1*time.Hour {
		at.policyAlert[policyName] = now
		return true
	}

	return false
}

func (at *AlertThrottle) SilencePolicy(policyName string) {
	at.mu.Lock()
	defer at.mu.Unlock()

	delete(at.policyAlert, policyName)
}