package api

import (
	"github.com/axentx/surrogate-1/src/api/middleware"
	"github.com/axentx/surrogate-1/src/api/routes"
	"github.com/gin-gonic/gin"
)

func SetupAPI(rateLimit, period int, apiKey string) *gin.Engine {
	router := gin.Default()

	rateLimiter := middleware.NewRateLimiter(rateLimit, period)
	router.Use(middleware.RateLimiter(rateLimiter))

	routes.initMetricsRoutes(router)

	return router
}