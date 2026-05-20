package routes

import (
	"surrogate-1/backend/controllers"

	"github.com/gin-gonic/gin"
)

// RegisterApprovalLinkRoutes registers the approval‑link related routes.
func RegisterApprovalLinkRoutes(r *gin.Engine) {
	links := r.Group("/api/v1/approval-links")
	{
		links.GET("/:id", controllers.GetApprovalLink)
		links.POST("/:id/decision", controllers.PostApprovalDecision)
	}
}