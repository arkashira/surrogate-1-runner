package controllers

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"

	"github.com/axentx/surrogate-1/backend/models"
	"github.com/axentx/surrogate-1/backend/repositories"
	"github.com/axentx/surrogate-1/backend/utils"
)

// DecisionRequest represents the JSON payload for a decision
type DecisionRequest struct {
	Status  string `json:"status"`  // "approve" or "reject"
	Comment string `json:"comment,omitempty"`
}

// DecisionResponse represents the JSON response after decision
type DecisionResponse struct {
	Message string `json:"message"`
}

// PostDecision handles POST /api/v1/approval-links/{id}/decision
func PostDecision(w http.ResponseWriter, r *http.Request) {
	// 1️⃣  Parse and validate the approval‑link ID
	vars := mux.Vars(r)
	approvalID, err := strconv.ParseInt(vars["id"], 10, 64)
	if err != nil {
		utils.WriteError(w, http.StatusBadRequest, "invalid approval link id")
		return
	}

	// 2️⃣  Decode the request body
	var req DecisionRequest
	if err := json.NewDecoder(r.Body).Decode(&req); err != nil {
		utils.WriteError(w, http.StatusBadRequest, "invalid JSON payload")
		return
	}

	// 3️⃣  Validate the status field
	if req.Status != models.ApprovalStatusApprove && req.Status != models.ApprovalStatusReject {
		utils.WriteError(w, http.StatusBadRequest,
			"status must be 'approve' or 'reject'")
		return
	}

	// 4️⃣  Load the approval link
	link, err := repositories.GetApprovalLinkByID(approvalID)
	if err != nil {
		if err == repositories.ErrNotFound {
			utils.WriteError(w, http.StatusNotFound, "approval link not found")
		} else {
			utils.WriteError(w, http.StatusInternalServerError, "database error")
		}
		return
	}

	// 5️⃣  Enforce single‑use
	if link.DecidedAt.Valid {
		utils.WriteError(w, http.StatusForbidden,
			"decision already recorded")
		return
	}

	// 6️⃣  Persist the decision
	if err := repositories.RecordDecision(approvalID, req.Status, req.Comment); err != nil {
		utils.WriteError(w, http.StatusInternalServerError,
			"failed to record decision")
		return
	}

	// 7️⃣  Success response
	resp := DecisionResponse{Message: "decision recorded, thank you"}
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(http.StatusCreated)
	if err := json.NewEncoder(w).Encode(resp); err != nil {
		// unlikely, but guard against encoding failure
		utils.WriteError(w, http.StatusInternalServerError, "response encoding error")
	}
}