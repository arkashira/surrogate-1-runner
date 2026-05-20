package routes

import (
	"net/http"

	"github.com/gin-gonic/gin"
)

func initMetricsRoutes(router *gin.Engine) {
	metrics := router.Group("/v1/synthetic")
	{
		metrics.POST("/metrics", func(c *gin.Context) {
			// TODO: Implement metric generation and Datadog emission
			c.JSON(http.StatusAccepted, gin.H{"message": "Metric generation job started"})
		})

		jobs := metrics.Group("/jobs")
		{
			jobs.GET("/:id", func(c *gin.Context) {
				// TODO: Implement job status retrieval
				c.JSON(http.StatusOK, gin.H{"status": "queued"})
			})
		}
	}
}