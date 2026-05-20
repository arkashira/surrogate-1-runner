package relay

import (
	"bytes"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHandleTransactionRequest(t *testing.T) {
	tests := []struct {
		name     string
		chainID  string
		expected int
	}{
		{"Valid Chain ID", "1", http.StatusOK},
		{"Invalid Chain ID", "999", http.StatusBadRequest},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			reqBody := TransactionRequest{ChainID: tt.chainID}
			jsonData, _ := json.Marshal(reqBody)
			req := httptest.NewRequest("POST", "/transaction", bytes.NewBuffer(jsonData))
			w := httptest.NewRecorder()

			HandleTransactionRequest(w, req)

			if w.Code != tt.expected {
				t.Errorf("Expected status code %d, got %d", tt.expected, w.Code)
			}
		})
	}
}