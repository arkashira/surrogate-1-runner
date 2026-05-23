package main

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/axentx/surrogate-1/terraform_cost_data_api"
)

func main() {
	costDataService := &costDataService{
		costDataAPI: &terraform_cost_data_api.TerraformCostDataAPI{},
	}

	http.HandleFunc("/cost-data", costDataService.handleCostDataRequest)

	log.Fatal(http.ListenAndServe(":8080", nil))
}

type costDataService struct {
	costDataAPI *terraform_cost_data_api.TerraformCostDataAPI
}

func (s *costDataService) handleCostDataRequest(w http.ResponseWriter, r *http.Request) {
	if r.Method != "GET" {
		http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		return
	}

	costData, err := s.costDataAPI.GetCostData(r.Context())
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.Header().Set("Content-Type", "application/json")
	w.Write([]byte(fmt.Sprintf("%v", costData)))
}