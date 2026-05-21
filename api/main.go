package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/yourorg/surrogate-1/api/middleware"
)

func main() {
	r := mux.NewRouter()
	r.Use(middleware.SecurityMiddleware)

	http.Handle("/", r)

	log.Println("Starting server on :8080")
	err := http.ListenAndServe(":8080", nil)
	if err != nil {
		log.Fatal(err)
	}
}