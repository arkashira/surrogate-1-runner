package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"time"

	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/api/terraform-provider-aws/aws"
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/api/terraform-provider-aws/aws/external"
)

type TerraformCostDataAPI struct{}

func (t *TerraformCostDataAPI) GetCostData(ctx context.Context) (map[string]float64, error) {
	// Initialize AWS session
	sess, err := external.NewSession(ctx, &aws.Config{Region: aws.String("us-west-2")})
	if err != nil {
		return nil, err
	}

	// Create AWS cost explorer client
	costExplorer := sess.Client("costexplorer")

	// Set up cost explorer query
	params := &aws.CostExplorerQueryInput{
		TimePeriod: &aws.TimePeriod{
			Start: aws.String(time.Now().Add(-5 * time.Minute).Format(time.RFC3339)),
			End:   aws.String(time.Now().Format(time.RFC3339)),
		},
		Granularity: aws.String("MONTHLY"),
		Filters: []*aws.CostFilter{
			{
				Name: aws.String("SERVICE"),
				Values: []*string{
					aws.String("AmazonS3"),
				},
			},
		},
	}

	// Get cost data
	resp, err := costExplorer.GetCostAndUsageWithContext(ctx, params)
	if err != nil {
		return nil, err
	}

	// Parse cost data
	costData := make(map[string]float64)
	for _, group := range resp.Result {
		costData[group.Key] = group.Amount
	}

	return costData, nil
}

func (t *TerraformCostDataAPI) UpdateCostData(ctx context.Context) error {
	// Get cost data
	costData, err := t.GetCostData(ctx)
	if err != nil {
		return err
	}

	// Update cost data in database
	// (Implementation omitted for brevity)

	return nil
}

func main() {
	http.HandleFunc("/cost-data", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "GET" {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
			return
		}

		costDataAPI := &TerraformCostDataAPI{}
		costData, err := costDataAPI.GetCostData(r.Context())
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		w.Header().Set("Content-Type", "application/json")
		w.Write([]byte(fmt.Sprintf("%v", costData)))
	})

	log.Fatal(http.ListenAndServe(":8080", nil))
}