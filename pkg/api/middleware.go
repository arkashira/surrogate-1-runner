
package api

import (
	"net/http"
)

func ErrorHandler(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		next.ServeHTTP(w, r)

		if status := recover(); status != nil {
			http.Error(w, fmt.Sprintf("Internal server error: %v", status), http.StatusInternalServerError)
		}
	})
}