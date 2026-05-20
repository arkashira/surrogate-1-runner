package main

import (
	"database/sql"
	"fmt"
	"log"
	"net/http"

	_ "github.com/lib/pq"

	"/opt/axentx/surrogate-1/backend/policy"
)

func main() {
	db, err := sql.Open("postgres", "user:password@localhost/database")
	if err != nil {
		log.Fatal(err)
	}

	http.HandleFunc("/policies", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodPost {
			var policy policy.Policy
			err := json.NewDecoder(r.Body).Decode(&policy)
			if err != nil {
				http.Error(w, err.Error(), http.StatusBadRequest)
				return
			}

			err = policy.SavePolicy(db, policy)
			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}

			w.WriteHeader(http.StatusCreated)
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	http.HandleFunc("/policies/", func(w http.ResponseWriter, r *http.Request) {
		if r.Method == http.MethodGet {
			id := r.URL.Path[len("/policies/"):]
			policy, err := policy.GetPolicy(db, id)
			if err != nil {
				http.Error(w, err.Error(), http.StatusNotFound)
				return
			}

			json.NewEncoder(w).Encode(policy)
		} else {
			http.Error(w, "Method not allowed", http.StatusMethodNotAllowed)
		}
	})

	log.Fatal(http.ListenAndServe(":8080", policy.JSONValidationMiddleware(http.DefaultServeMux)))
}