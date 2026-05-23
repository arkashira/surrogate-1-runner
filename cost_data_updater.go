package main

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/axentx/surrogate-1/terraform_cost_data_api"
)

func main() {
	costDataUpdater := &costDataUpdater{
		costDataAPI: &terraform_cost_data_api.TerraformCostDataAPI{},
	}

	ticker := time.NewTicker(5 * time.Minute)
	defer ticker.Stop()

	for range ticker.C {
		err := costDataUpdater.UpdateCostData(context.Background())
		if err != nil {
			log.Println(err)
		}
	}
}

type costDataUpdater struct {
	costDataAPI *terraform_cost_data_api.TerraformCostDataAPI
}