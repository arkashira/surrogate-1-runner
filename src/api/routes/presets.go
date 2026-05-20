package routes

import (
	"encoding/json"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
	"github.com/sirupsen/logrus"

	"github.com/axentx/surrogate-1/internal/models"
	"github.com/axentx/surrogate-1/internal/services"
	"github.com/axentx/surrogate-1/internal/utils"
)

// Preset represents a synthetic metric pattern preset
type Preset struct {
	ID              string    `json:"id"`
	Name            string    `json:"name"`
	MetricType      string    `json:"metric_type"`
	ValueDistribution string   `json:"value_distribution"`
	Value           float64   `json:"value"`
	Interval        int       `json:"interval"`
	CreatedAt       string    `json:"created_at"`
}

// PresetList represents a list of presets
type PresetList []Preset

// PresetHandler handles preset operations
type PresetHandler struct {
	presetService *services.PresetService
	logger        *logrus.Logger
}

// NewPresetHandler creates a new PresetHandler
func NewPresetHandler(presetService *services.PresetService, logger *logrus.Logger) *PresetHandler {
	return &PresetHandler{
		presetService: presetService,
		logger:        logger,
	}
}

// GetPresets handles GET /presets
func (h *PresetHandler) GetPresets(w http.ResponseWriter, r *http.Request) {
	presets, err := h.presetService.ListPresets()
	if err != nil {
		h.logger.Errorf("failed to get presets: %v", err)
		utils.WriteError(w, http.StatusInternalServerError, "Failed to retrieve presets")
		return
	}

	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(PresetList(presets))
}

// CreatePreset handles POST /presets
func (h *PresetHandler) CreatePreset(w http.ResponseWriter, r *http.Request) {
	var preset models.Preset
	if err := json.NewDecoder(r.Body).Decode(&preset); err != nil {
		utils.WriteError(w, http.StatusBadRequest, "Invalid request body")
		return
	}

	if err := h.presetService.CreatePreset(preset); err != nil {
		h.logger.Errorf("failed to create preset: %v", err)
		utils.WriteError(w, http.StatusInternalServerError, "Failed to create preset")
		return
	}

	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(preset)
}

// UpdatePreset handles PUT /presets/{id}
func (h *PresetHandler) UpdatePreset(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	var preset models.Preset
	if err := json.NewDecoder(r.Body).Decode(&preset); err != nil {
		utils.WriteError(w, http.StatusBadRequest, "Invalid request body")
		return
	}

	preset.ID = id

	if err := h.presetService.UpdatePreset(preset); err != nil {
		h.logger.Errorf("failed to update preset: %v", err)
		utils.WriteError(w, http.StatusInternalServerError, "Failed to update preset")
		return
	}

	w.WriteHeader(http.StatusOK)
	json.NewEncoder(w).Encode(preset)
}

// DeletePreset handles DELETE /presets/{id}
func (h *PresetHandler) DeletePreset(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id := vars["id"]

	if err := h.presetService.DeletePreset(id); err != nil {
		h.logger.Errorf("failed to delete preset: %v", err)
		utils.WriteError(w, http.StatusInternalServerError, "Failed to delete preset")
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// RegisterPresetRoutes registers preset routes
func RegisterPresetRoutes(router *mux.Router, presetService *services.PresetService, logger *logrus.Logger) {
	handler := NewPresetHandler(presetService, logger)

	router.HandleFunc("/presets", handler.GetPresets).Methods("GET")
	router.HandleFunc("/presets", handler.CreatePreset).Methods("POST")
	router.HandleFunc("/presets/{id}", handler.UpdatePreset).Methods("PUT")
	router.HandleFunc("/presets/{id}", handler.DeletePreset).Methods("DELETE")
}