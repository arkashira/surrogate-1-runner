package database

import (
	"context"
	"fmt"
	"log"

	"github.com/axentx/axentx-lib/models"
)

func (db *Database) GetProviderCosts(startDate, endDate string) ([]models.ProviderCost, error) {
	// implement database query to get provider costs
	return nil, nil
}

func (db *Database) GetProviderCostsByWeek(startDate, endDate string) ([]models.ProviderCost, error) {
	// implement database query to get provider costs by week
	return nil, nil
}

func (db *Database) FilterProviderCosts(startDate, endDate string) ([]models.ProviderCost, error) {
	// implement database query to filter provider costs
	return nil, nil
}