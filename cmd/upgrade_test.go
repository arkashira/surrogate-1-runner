package cmd

import (
	"bytes"
	"context"
	"testing"
	"time"

	"github.com/spf13/cobra"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/axentx/surrogate-1/pkg/upgrade"
)

// ---------------------------------------------------------------------------
// Helper – execute a cobra command and capture stdout/stderr
// ---------------------------------------------------------------------------
func runCommand(cmd *cobra.Command, args ...string) (string, error) {
	var buf bytes.Buffer
	cmd.SetOut(&buf)
	cmd.SetErr(&buf)
	cmd.SetArgs(args)
	err := cmd.Execute()
	return buf.String(), err
}

// ---------------------------------------------------------------------------
// CLI tests – cover valid, invalid and missing target flags
// ---------------------------------------------------------------------------
func TestUpgradeCommand_ValidVersion(t *testing.T) {
	out, err := runCommand(NewUpgradeCmd(), "--target", "v1.26.0")
	require.NoError(t, err)
	assert.Contains(t, out, "Starting upgrade to v1.26.0")
}

func TestUpgradeCommand_InvalidVersion(t *testing.T) {
	out, err := runCommand(NewUpgradeCmd(), "--target", "v0.0.0")
	require.Error(t, err)
	assert.Contains(t, out, "unsupported Kubernetes version")
}

func TestUpgradeCommand_NoTarget(t *testing.T) {
	out, err := runCommand(NewUpgradeCmd())
	require.Error(t, err)
	assert.Contains(t, out, `required flag "target"`)
}

// ---------------------------------------------------------------------------
// Engine tests – success, failure and timestamp logging
// ---------------------------------------------------------------------------
func TestEngine_Start_Success(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	// Use a real engine but replace the internal start hook so we can observe it
	engine := upgrade.NewEngine()
	var loggedMsg string
	engine.OnStart = func(ctx context.Context, target string) error {
		loggedMsg = "engine started"
		return nil
	}

	err := engine.Start(ctx, "v1.26.0")
	require.NoError(t, err)
	assert.Equal(t, "engine started", loggedMsg)
}

func TestEngine_Start_Failure(t *testing.T) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	engine := upgrade.NewEngine()
	engine.OnStart = func(ctx context.Context, target string) error {
		return upgrade.ErrUpgradeFailed
	}

	err := engine.Start(ctx, "v1.26.0")
	require.Error(t, err)
	assert.Equal(t, upgrade.ErrUpgradeFailed, err)
}

func TestEngine_Start_Timestamp(t *testing.T) {
	// The real engine records the start time in a field called `startedAt`.
	// We assert that the field is set after Start() returns.
	engine := upgrade.NewEngine()
	start := time.Now()
	_ = engine.Start(context.Background(), "v1.26.0")
	require.False(t, engine.StartedAt.IsZero(), "startedAt should be set")
	assert.True(t, engine.StartedAt.After(start), "startedAt should be after the call")
}