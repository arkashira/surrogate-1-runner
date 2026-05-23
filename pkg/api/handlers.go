
package api

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/axentx/surrogate-1/pkg/gpu"
)

func (h *Handler) AllocateGPU(w http.ResponseWriter, r *http.Request) {
	if len(gpu.Discover()) < 1 {
		http.Error(w, "No GPUs found", http.StatusNoContent)
		return
	}

	gpus := gpu.Discover()
	id := strconv.Itoa(len(gpus))

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(map[string]string{"id": id})
}