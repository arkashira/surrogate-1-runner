package controllers

import (
	"net/http"

	"surrogate-1/backend/database"
	"surrogate-1/backend/models"

	"github.com/gin-gonic/gin"
)

// GetApprovalLink handles GET /api/v1/approval-links/:id
func GetApprovalLink(c *gin.Context) {
	id := c.Param("id")

	link, err := database.GetApprovalLinkByID(id)
	if err != nil {
		if err == database.ErrNotFound {
			c.JSON(http.StatusNotFound, gin.H{
				"error": "approval link not found",
			})
		} else {
			c.JSON(http.StatusInternalServerError, gin.H{
				"error": "internal server error",
			})
		}
		return
	}

	c.JSON(http.StatusOK, link)
}

// PostApprovalDecision handles POST /api/v1/approval-links/:id/decision
func PostApprovalDecision(c *gin.Context) {
	id := c.Param("id")

	// Validate request body
	var payload struct {
		Status  string `json:"status" binding:"required,oneof=approve reject"`
		Comment string `json:"comment"`
	}
	if err := c.ShouldBindJSON(&payload); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{
			"error": err.Error(),
		})
		return
	}

	// In a real system you would persist the decision here.
	// For now we just echo it back.
	c.JSON(http.StatusOK, gin.H{
		"id":      id,
		"status":  payload.Status,
		"comment": payload.Comment,
		"message": "Decision recorded",
	})
}