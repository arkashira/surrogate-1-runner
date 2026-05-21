package middleware

import (
	"log"
	"net/http"
	"regexp"
)

var sqlInjectionPattern = regexp.MustCompile(`(?i)(?:')|(?:--)|(?:#.*=)|(?:/\*.*?\*/)|(%7C|%27|%5C)`)

func SecurityMiddleware(next http.Handler) http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		body := r.Body
		defer body.Close()

		if sqlInjectionPattern.MatchString(r.URL.Path) || sqlInjectionPattern.MatchString(r.Method) {
			log.Println("SQL Injection detected:", r.URL.Path, r.Method)
			http.Error(w, "Forbidden", http.StatusForbidden)
			return
		}

		next.ServeHTTP(w, r)
	})
}