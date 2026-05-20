package database

import (
	"context"
	"database/sql"
	"encoding/json"
	"fmt"

	"github.com/axentx/surrogate-1/api"
)

type AlertConfig struct {
	ProjectID   string  `json:"project_id"`
	BudgetLimit float64 `json:"budget_limit"`
	WebhookURLs []string `json:"webhook_urls"`
}

func GetAlertConfig(projectID string) (*AlertConfig, error) {
	db := api.GetDB()
	ctx := context.Background()

	var configJSON string
	err := db.QueryRowContext(
		ctx,
		"SELECT JSON_BUILD_OBJECT('project_id', project_id, 'budget_limit', budget_limit, 'webhook_urls', webhook_urls)::text FROM alert_configs WHERE project_id = $1",
		projectID,
	).Scan(&configJSON)

	if err != nil {
		if err == sql.ErrNoRows {
			return nil, fmt.Errorf("no configuration found for project %s", projectID)
		}
		return nil, fmt.Errorf("database query failed: %w", err)
	}

	var config AlertConfig
	if err := json.Unmarshal([]byte(configJSON), &config); err != nil {
		return nil, fmt.Errorf("failed to parse config: %w", err)
	}

	return &config, nil
}