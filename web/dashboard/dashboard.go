package dashboard

import (
	"context"
	"fmt"
	"log"
	"net/http"

	"github.com/axentx/axentx-lib/database"
	"github.com/axentx/axentx-lib/models"
	"github.com/gorilla/mux"
)

func (d *Dashboard) GetProviderCostsHandler(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	startDate := r.URL.Query().Get("start_date")
	endDate := r.URL.Query().Get("end_date")

	if startDate == "" || endDate == "" {
		http.Error(w, "start_date and end_date are required", http.StatusBadRequest)
		return
	}

	costs, err := d.db.GetProviderCosts(startDate, endDate)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(costs)
}

func (d *Dashboard) GetProviderCostsByWeekHandler(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	startDate := r.URL.Query().Get("start_date")
	endDate := r.URL.Query().Get("end_date")

	if startDate == "" || endDate == "" {
		http.Error(w, "start_date and end_date are required", http.StatusBadRequest)
		return
	}

	costs, err := d.db.GetProviderCostsByWeek(startDate, endDate)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(costs)
}

func (d *Dashboard) FilterProviderCostsHandler(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	startDate := r.URL.Query().Get("start_date")
	endDate := r.URL.Query().Get("end_date")

	if startDate == "" || endDate == "" {
		http.Error(w, "start_date and end_date are required", http.StatusBadRequest)
		return
	}

	costs, err := d.db.FilterProviderCosts(startDate, endDate)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	json.NewEncoder(w).Encode(costs)
}