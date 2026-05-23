package middleware

import (
	"net/http"
	"strings"

	"github.com/axentx/surrogate-1/pkg/auth"
)

func AuthSSOMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		// Check if the request path starts with /admin
		if strings.HasPrefix(r.URL.Path, "/admin") {
			// Validate SSO token
			token := r.Header.Get("Authorization")
			if token == "" {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}

			// Validate the token using the auth package
			valid, err := auth.ValidateToken(token)
			if err != nil || !valid {
				http.Error(w, "Unauthorized", http.StatusUnauthorized)
				return
			}
		}

		// Call the next handler
		next.ServeHTTP(w, r)
	})
}