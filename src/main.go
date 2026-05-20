package main

import (
	"context"
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/axentx/surrogate-1/pkg/auth"
)

func main() {
	r := mux.NewRouter()
	a := auth.NewAuthMiddleware()
	r.Use(a.AuthMiddleware)
	r.HandleFunc("/api/v1/mappings", api.GetMappings).Methods("GET")
	r.HandleFunc("/api/v1/mappings", api.AddMapping).Methods("POST")
	r.HandleFunc("/api/v1/mappings/{service_name}", api.DeleteMapping).Methods("DELETE")
	log.Fatal(http.ListenAndServe(":8080", r))
}