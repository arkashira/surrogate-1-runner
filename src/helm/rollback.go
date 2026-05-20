package helm

import (
	"bytes"
	"context"
	"fmt"
	"os/exec"
	"time"

	"github.com/jmoiron/sqlx"
	"github.com/sirupsen/logrus"
)

// RollbackConfig holds the parameters needed to perform a Helm rollback.
type RollbackConfig struct {
	// ReleaseName is the name of the Helm release to rollback.
	ReleaseName string
	// Namespace is the Kubernetes namespace where the release resides.
	Namespace string
	// TargetRevision is the revision number to rollback to. If empty, Helm will
	// rollback to the previous revision automatically.
	TargetRevision string
	// HelmBinary is the path to the Helm executable. Defaults to "helm".
	HelmBinary string
	// Timeout is the maximum duration to wait for the rollback to complete.
	Timeout time.Duration
	// Logger is a logrus logger used for all output. If nil, logrus.StandardLogger() is used.
	Logger *logrus.Logger
	// DB is an optional sqlx.DB used to persist rollback actions. If nil, no DB writes occur.
	DB *sqlx.DB
}

// rollbackAction represents a row in the helm_rollback_actions table.
type rollbackAction struct {
	ID            int64     `db:"id"`
	ReleaseName   string    `db:"release_name"`
	Namespace     string    `db:"namespace"`
	TargetRevision int      `db:"target_revision"`
	AttemptedAt   time.Time `db:"attempted_at"`
	CompletedAt   time.Time `db:"completed_at"`
	Succeeded     bool      `db:"succeeded"`
	ErrorMessage  string    `db:"error_message"`
}

// Rollback performs a Helm rollback using the provided configuration.
// It records the attempt in the database (if DB is set) and streams
// stdout/stderr to the supplied logger.
func Rollback(ctx context.Context, cfg RollbackConfig) error {
	if cfg.Logger == nil {
		cfg.Logger = logrus.StandardLogger()
	}
	if cfg.HelmBinary == "" {
		cfg.HelmBinary = "helm"
	}

	// Build the command arguments.
	args := []string{"rollback", cfg.ReleaseName}
	if cfg.TargetRevision != "" {
		args = append(args, cfg.TargetRevision)
	}
	if cfg.Namespace != "" {
		args = append(args, "--namespace", cfg.Namespace)
	}
	if cfg.Timeout > 0 {
		args = append(args, "--timeout", fmt.Sprintf("%ds", int(cfg.Timeout.Seconds())))
	}

	// Prepare the command.
	cmd := exec.CommandContext(ctx, cfg.HelmBinary, args...)
	var stdout, stderr bytes.Buffer
	cmd.Stdout = &stdout
	cmd.Stderr = &stderr

	// Log the start of the rollback.
	cfg.Logger.WithFields(logrus.Fields{
		"release":   cfg.ReleaseName,
		"namespace": cfg.Namespace,
		"revision":  cfg.TargetRevision,
		"timeout":   cfg.Timeout,
		"helm_bin":  cfg.HelmBinary,
	}).Info("starting helm rollback")

	// Persist the attempt (if a DB is configured).
	if cfg.DB != nil {
		_, err := cfg.DB.ExecContext(ctx, `
			INSERT INTO helm_rollback_actions
				(release_name, namespace, target_revision, attempted_at)
			VALUES ($1, $2, $3, $4)
		`, cfg.ReleaseName, cfg.Namespace, cfg.TargetRevision, time.Now())
		if err != nil {
			cfg.Logger.WithError(err).Warn("failed to log rollback attempt")
		}
	}

	// Run the command.
	if err := cmd.Start(); err != nil {
		return fmt.Errorf("failed to start helm rollback: %w", err)
	}

	done := make(chan error, 1)
	go func() { done <- cmd.Wait() }()

	var err error
	select {
	case <-ctx.Done():
		_ = cmd.Process.Kill()
		err = fmt.Errorf("helm rollback cancelled: %w", ctx.Err())
	case err = <-done:
		if err != nil {
			err = fmt.Errorf("helm rollback failed: %w", err)
		}
	}

	// Log output.
	if stdout.Len() > 0 {
		cfg.Logger.Info(stdout.String())
	}
	if stderr.Len() > 0 {
		cfg.Logger.Error(stderr.String())
	}

	// Persist the result (if a DB is configured).
	if cfg.DB != nil {
		succeeded := err == nil
		_, updErr := cfg.DB.ExecContext(ctx, `
			UPDATE helm_rollback_actions
			SET succeeded = $1,
			    completed_at = $2,
			    error_message = $3
			WHERE release_name = $4
			  AND namespace = $5
			  AND target_revision = $6
			  AND attempted_at = $7
		`, succeeded, time.Now(), stderr.String(), cfg.ReleaseName, cfg.Namespace, cfg.TargetRevision, time.Now().Add(-time.Minute))
		if updErr != nil {
			cfg.Logger.WithError(updErr).Warn("failed to update rollback record")
		}
	}

	return err
}