package compliance

import (
	"testing"
	"time"
)

func TestAlertThrottle(t *testing.T) {
	at := NewAlertThrottle()
	policyName := "test-policy"

	// First alert should be allowed
	if !at.ShouldAlert(policyName) {
		t.Error("Expected first alert to be allowed")
	}

	// Second alert within the same hour should be throttled
	if at.ShouldAlert(policyName) {
		t.Error("Expected alert to be throttled within the same hour")
	}

	// Alert after an hour should be allowed
	time.Sleep(1 * time.Second) // Simulate time passage
	at.policyAlert[policyName] = time.Now().Add(-1 * time.Hour)
	if !at.ShouldAlert(policyName) {
		t.Error("Expected alert to be allowed after an hour")
	}

	// Test silencing a policy
	at.SilencePolicy(policyName)
	if !at.ShouldAlert(policyName) {
		t.Error("Expected alert to be allowed after silencing the policy")
	}
}