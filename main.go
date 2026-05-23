
package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/axentx/surrogate-1/pkg/api"
)

func main() {
	router := mux.NewRouter()
	router.Use(api.ErrorHandler)

	router.HandleFunc("/api/v1/gpu", api.AllocateGPU).Methods("GET")

	log.Fatal(http.ListenAndServe(":8080", router))
}