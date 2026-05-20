package policy

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	_ "github.com/lib/pq"
)

type Policy struct {
	ID          int    `json:"id"`
	Version     int    `json:"version"`
	Conditions  string `json:"conditions"`
	CreatedAt   string `json:"created_at"`
	UpdatedAt   string `json:"updated_at"`
}

type PolicyService struct {
	db *sql.DB
}

func NewPolicyService(db *sql.DB) *PolicyService {
	return &PolicyService{db: db}
}

func (s *PolicyService) CreatePolicy(c *gin.Context) {
	var policy Policy
	if err := c.ShouldBindJSON(&policy); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	_, err := s.db.Exec("INSERT INTO policies (conditions) VALUES ($1)", policy.Conditions)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusCreated, policy)
}

func (s *PolicyService) GetPolicy(c *gin.Context) {
	id := c.Params.ByName("id")
	var policy Policy
	row := s.db.QueryRow("SELECT id, version, conditions, created_at, updated_at FROM policies WHERE id=$1", id)
	err := row.Scan(&policy.ID, &policy.Version, &policy.Conditions, &policy.CreatedAt, &policy.UpdatedAt)
	if err == sql.ErrNoRows {
		c.JSON(http.StatusNotFound, gin.H{"error": "Policy not found"})
		return
	} else if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, policy)
}

func (s *PolicyService) UpdatePolicy(c *gin.Context) {
	id := c.Params.ByName("id")
	var policy Policy
	if err := c.ShouldBindJSON(&policy); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	_, err := s.db.Exec("UPDATE policies SET conditions=$1 WHERE id=$2", policy.Conditions, id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusOK, policy)
}

func (s *PolicyService) DeletePolicy(c *gin.Context) {
	id := c.Params.ByName("id")
	_, err := s.db.Exec("DELETE FROM policies WHERE id=$1", id)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": err.Error()})
		return
	}

	c.JSON(http.StatusNoContent, nil)
}

func (s *PolicyService) ValidatePolicy(c *gin.Context) {
	var policy Policy
	if err := c.ShouldBindJSON(&policy); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": err.Error()})
		return
	}

	// Add validation logic here
	if policy.Conditions == "" {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Conditions cannot be empty"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"message": "Policy is valid"})
}