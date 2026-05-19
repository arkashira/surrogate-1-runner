package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/axentx/surrogate-1/api/routes"
)

func main() {
	router := mux.NewRouter()

	routes.SetupCoverageRoutes(router)

	log.Println("Starting server on :8080")
	http.ListenAndServe(":8080", router)
}