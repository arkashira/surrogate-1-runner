package tests

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestMFARecoveryIntegrationSuite(t *testing.T) {
	t.Run("TestMFARecoveryIntegrationWithExistingAuthentication", TestMFARecoveryIntegrationWithExistingAuthentication)
}