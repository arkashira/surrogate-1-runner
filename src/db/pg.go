package db

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"
	"os"
	"sync"
	"time"

	_ "github.com/lib/pq" // PostgreSQL driver
	"opt/axentx/surrogate-1/src/model"
)

var (
	once sync.Once
	pool *sql.DB
)

// Init creates (once) a *sql.DB pool using environment variables.
// It is safe for concurrent callers and returns the same instance every time.
func Init() (*sql.DB, error) {
	var err error
	once.Do(func() {
		// Environment‑based configuration – works out‑of‑the‑box in most containers.
		host := getenv("PGHOST", "localhost")
		port := getenv("PGPORT", "5432")
		user := getenv("PGUSER", "postgres")
		password := getenv("PGPASSWORD", "")
		dbname := getenv("PGDATABASE", "surrogate")
		sslmode := getenv("PGSSLMODE", "disable") // allow override

		dsn := fmt.Sprintf(
			"host=%s port=%s user=%s password=%s dbname=%s sslmode=%s",
			host, port, user, password, dbname, sslmode,
		)

		pool, err = sql.Open("postgres", dsn)
		if err != nil {
			return
		}
		// Reasonable defaults – adjust as needed.
		pool.SetMaxOpenConns(25)
		pool.SetMaxIdleConns(5)
		pool.SetConnMaxLifetime(5 * time.Minute)

		// Verify the connection early.
		if pingErr := pool.Ping(); pingErr != nil {
			err = fmt.Errorf("postgres ping failed: %w", pingErr)
			return
		}
	})
	return pool, err
}

// Get returns the already‑initialized *sql.DB.
// Panics if Init has not been called successfully – this mirrors the behaviour
// of many popular singleton helpers and surfaces programmer error early.
func Get() *sql.DB {
	if pool == nil {
		panic("database not initialized; call db.Init() first")
	}
	return pool
}

// New creates a PG wrapper from an explicit DSN.  This is useful when the
// caller wants to manage multiple connections or avoid the env‑var defaults.
func New(dsn string) (*PG, error) {
	db, err := sql.Open("postgres", dsn)
	if err != nil {
		return nil, fmt.Errorf("open postgres: %w", err)
	}
	if err = db.Ping(); err != nil {
		return nil, fmt.Errorf("ping postgres: %w", err)
	}
	return &PG{db: db}, nil
}

// PG is a thin repository object that owns a *sql.DB.
type PG struct {
	db *sql.DB
}

// Close shuts down the underlying connection pool.
func (p *PG) Close() error { return p.db.Close() }

// InsertDriftEvent persists a DriftEvent and returns the generated primary key.
// It accepts a context for cancellation/timeout propagation.
func (p *PG) InsertDriftEvent(ctx context.Context, ev *model.DriftEvent) (int64, error) {
	if ev == nil {
		return 0, fmt.Errorf("nil drift event")
	}
	// Auto‑populate timestamp if the caller left it zero.
	if ev.DetectedAt.IsZero() {
		ev.DetectedAt = time.Now().UTC()
	}

	// Normalise DiffDetails to []byte (json.RawMessage) – callers may have passed a Go value.
	var diffJSON []byte
	switch v := ev.DiffDetails.(type) {
	case []byte:
		diffJSON = v
	case json.RawMessage:
		diffJSON = []byte(v)
	default:
		b, err := json.Marshal(v)
		if err != nil {
			return 0, fmt.Errorf("marshal diff details: %w", err)
		}
		diffJSON = b
	}

	const stmt = `
		INSERT INTO api_drift_events (detected_at, service, diff_details)
		VALUES ($1, $2, $3)
		RETURNING id
	`
	var id int64
	if err := p.db.QueryRowContext(ctx, stmt, ev.DetectedAt, ev.Service, diffJSON).Scan(&id); err != nil {
		return 0, fmt.Errorf("insert drift event: %w", err)
	}
	ev.ID = id
	return id, nil
}

// Helper – read env var with fallback.
func getenv(key, fallback string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return fallback
}