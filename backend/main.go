package main

import (
	"log"

	"github.com/gin-gonic/gin"
	"surrogate-1/backend/routes"
)

func main() {
	r := gin.Default()

	// Register all approval‑link routes
	routes.RegisterApprovalLinkRoutes(r)

	// TODO: register other route groups here

	if err := r.Run(":8080"); err != nil {
		log.Fatalf("Server failed: %v", err)
	}
}