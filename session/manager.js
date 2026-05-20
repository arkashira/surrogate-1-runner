
const jwt = require('jsonwebtoken');
const moment = require('moment');

// ... (existing code)

function createSessionToken(userId) {
  // ... (existing code)

  const expiresAt = moment().add(24, 'hours').unix();

  return jwt.sign({ userId, expiresAt }, process.env.SESSION_SECRET, { expiresIn: '24h' });
}

// ... (existing code)

// opt/axentx/surrogate-1/middleware/auth_middleware.go

package middleware

import (
  "fmt"
  "net/http"
  "time"

  "github.com/dgrijalva/jwt-go"
  "github.com/gorilla/mux"
)

// ... (existing code)

func AuthMiddleware(next http.Handler) http.Handler {
  // ... (existing code)

  func(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
      // ... (existing code)

      tokenString := r.Header.Get("Authorization")
      if tokenString == "" {
        http.Error(w, "Missing or invalid token", http.StatusUnauthorized)
        return
      }

      token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
        if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
          return nil, fmt.Errorf("Unexpected signing method: %v", token.Header["alg"])
        }
        return []byte(process.Env("SESSION_SECRET")), nil
      })

      if err != nil {
        http.Error(w, "Invalid token", http.StatusUnauthorized)
        return
      }

      if claims, ok := token.Claims.(jwt.MapClaims); ok && token.Valid {
        userId := claims["userId"].(string)

        // ... (existing code)

        // Check if session is active
        lastActivity := sessionStore.Get(sessionId)
        if lastActivity.Time.After(time.Unix(int64(claims["expiresAt"].(float64)), 0)) {
          http.Error(w, "Session expired", http.StatusUnauthorized)
          return
        }

        // ... (existing code)
      } else {
        http.Error(w, "Invalid token", http.StatusUnauthorized)
      }

      next.ServeHTTP(w, r)
    })
  }(next)
}

// ... (existing code)