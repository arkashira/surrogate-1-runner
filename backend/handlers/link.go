package handlers

import (
	"net/http"

	"github.com/gorilla/mux"
	"github.com/surrogate-1/backend/utils"
)

func GenerateLinkHandler(w http.ResponseWriter, r *http.Request) {
	// In a real app these would come from the request or database.
	fileID     := "file-123"
	requestorID := "requestor-123"
	expiration := 48 * 60 * 60 // 48 hours in seconds

	link := utils.GenerateLink(fileID, requestorID, expiration)

	w.Header().Set("Content-Type", "image/png")
	if err := utils.GenerateQRCodeToWriter(link, w); err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}

// Register the route
func RegisterLinkRoutes(router *mux.Router) {
	router.HandleFunc("/link", GenerateLinkHandler).Methods(http.MethodGet)
}