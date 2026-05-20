package db

import (
	"context"
	"time"

	"github.com/jackc/pgx/v5/pgxpool"
)

var pool *pgxpool.Pool

// Init creates a global connection pool. Call it once at startup.
func Init(connString string) error {
	var err error
	pool, err = pgxpool.New(context.Background(), connString)
	return err
}

// DriftRow mirrors the columns we need from the `drifts` table.
type DriftRow struct {
	Service    string
	Deployment string
	Timestamp  time.Time
	Diff       string
}

// GetRecentDrifts returns up to `limit` most‑recent drift events ordered by timestamp descending.
func GetRecentDrifts(ctx context.Context, limit int) ([]DriftRow, error) {
	const query = `
		SELECT service, deployment, timestamp, diff
		FROM drifts
		ORDER BY timestamp DESC
		LIMIT $1;
	`

	// Enforce a sane query timeout (5 s) even if the caller passed a background context.
	rows, err := execWithTimeout(ctx, query, limit)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var results []DriftRow
	for rows.Next() {
		var dr DriftRow
		if err := rows.Scan(&dr.Service, &dr.Deployment, &dr.Timestamp, &dr.Diff); err != nil {
			return nil, err
		}
		results = append(results, dr)
	}
	if rows.Err() != nil {
		return nil, rows.Err()
	}
	return results, nil
}

// execWithTimeout runs a query with a 5‑second deadline.
// It is used by all DB helpers to guarantee that no query hangs indefinitely.
func execWithTimeout(parentCtx context.Context, sql string, args ...any) (pgx.Rows, error) {
	ctx, cancel := context.WithTimeout(parentCtx, 5*time.Second)
	// The cancel will fire when the query finishes or the deadline expires.
	// Defer is not used here because we return the rows; the caller must close them.
	// The cancel is still needed to release resources if the caller abandons the rows.
	// It will be called automatically when rows.Close() is invoked.
	go func() {
		<-ctx.Done()
		cancel()
	}()
	return pool.Query(ctx, sql, args...)
}