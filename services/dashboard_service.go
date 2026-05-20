package services

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/axentx/axentx-lib/database"
	"github.com/axentx/axentx-lib/models"
)

func (s *DashboardService) GetProviderCosts(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	startDate := r.URL.Query().Get("start_date")
	endDate := r.URL.Query().Get("end_date")

	if startDate == "" || endDate == "" {
		http.Error(w, "start_date and end_date are required", http.StatusBadRequest)
		return
	}

	costs, err := s.db.GetProviderCosts(startDate, endDate)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(costs)
}

func (s *DashboardService) GetProviderCostsByWeek(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	startDate := r.URL.Query().Get("start_date")
	endDate := r.URL.Query().Get("end_date")

	if startDate == "" || endDate == "" {
		http.Error(w, "start_date and end_date are required", http.StatusBadRequest)
		return
	}

	costs, err := s.db.GetProviderCostsByWeek(startDate, endDate)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(costs)
}

func (s *DashboardService) FilterProviderCosts(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	startDate := r.URL.Query().Get("start_date")
	endDate := r.URL.Query().Get("end_date")

	if startDate == "" || endDate == "" {
		http.Error(w, "start_date and end_date are required", http.StatusBadRequest)
		return
	}

	costs, err := s.db.FilterProviderCosts(startDate, endDate)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(costs)
}