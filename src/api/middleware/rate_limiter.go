package middleware

import (
	"net/http"
	"time"

	"github.com/gin-gonic/gin"
	"golang.org/x/time/rate"
)

func RateLimiter(rateLimiter *rate.Limiter) gin.HandlerFunc {
	return func(c *gin.Context) {
		if !rateLimiter.Allow() {
			c.AbortWithStatusJSON(http.StatusTooManyRequests, gin.H{"message": "Too many requests. Please try again later."})
			return
		}
		c.Next()
	}
}

func NewRateLimiter(rateLimit, period time.Duration) *rate.Limiter {
	return rate.NewLimiter(rate.Every(period), rateLimit)
}