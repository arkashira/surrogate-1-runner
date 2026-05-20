package api

import (
	"context"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/axentx/surrogate-1/pkg/auth"
)

type Mapping struct {
	Service string `json:"service"`
	Port    int    `json:"port"`
}

type Mappings struct {
	Mappings []Mapping `json:"mappings"`
}

func (a *Mappings) GetMappings(w http.ResponseWriter, r *http.Request) {
	mappings := auth.GetMappings()
	json.NewEncoder(w).Encode(mappings)
}

func (a *Mappings) AddMapping(w http.ResponseWriter, r *http.Request) {
	var mapping Mapping
	err := json.NewDecoder(r.Body).Decode(&mapping)
	if err != nil {
		http.Error(w, "Invalid payload", http.StatusBadRequest)
		return
	}
	auth.AddMapping(mapping.Service, mapping.Port)
	w.WriteHeader(http.StatusCreated)
}

func (a *Mappings) DeleteMapping(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	auth.DeleteMapping(vars["service_name"])
	w.WriteHeader(http.StatusNoContent)
}