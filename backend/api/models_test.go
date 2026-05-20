package api

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestGetModels(t *testing.T) {
	req, err := http.NewRequest("GET", "/api/models", nil)
	if err != nil {
		t.Fatal(err)
	}

	rr := httptest.NewRecorder()
	handler := http.HandlerFunc(GetModels)

	handler.ServeHTTP(rr, req)

	if status := rr.Code; status != http.StatusOK {
		t.Errorf("handler returned wrong status code: got %v want %v",
			status, http.StatusOK)
	}

	expected := []Model{
		{
			Name:             "Model0",
			Version:          "v1.0",
			ComplianceStatus: "Pass",
			LastAuditTime:    time.Now(),
		},
		// Add more expected models as needed
	}

	var models []Model
	err = json.Unmarshal(rr.Body.Bytes(), &models)
	if err != nil {
		t.Fatal(err)
	}

	if !reflect.DeepEqual(models, expected) {
		t.Errorf("handler returned unexpected body: got %v want %v",
			models, expected)
	}
}