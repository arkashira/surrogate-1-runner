package api

import (
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestGetComplianceStatus(t *testing.T) {
	tests := []struct {
		name     string
		expected ComplianceStatus
	}{
		{
			name: "Compliant Deployment",
			expected: ComplianceStatus{
				Status:            "compliant",
				Message:           "Deployment is compliant",
			},
		},
		{
			name: "Non-Compliant Deployment",
			expected: ComplianceStatus{
				Status:            "non-compliant",
				Message:           "Deployment is non-compliant",
				PolicyViolations:  []string{"Policy X violated"},
			},
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			req, err := http.NewRequest("GET", "/compliance/status", nil)
			if err != nil {
				t.Fatal(err)
			}

			rr := httptest.NewRecorder()
			handler := http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				if tt.name == "Non-Compliant Deployment" {
					checkCompliance = func() ComplianceStatus {
						return ComplianceStatus{
							Status:            "non-compliant",
							Message:           "Deployment is non-compliant",
							PolicyViolations:  []string{"Policy X violated"},
						}
					}
				}
				GetComplianceStatus(w, r)
			})

			handler.ServeHTTP(rr, req)

			if status := rr.Code; status != http.StatusOK {
				t.Errorf("handler returned wrong status code: got %v want %v", status, http.StatusOK)
			}

			var response ComplianceStatus
			err = json.Unmarshal(rr.Body.Bytes(), &response)
			if err != nil {
				t.Errorf("failed to unmarshal response: %v", err)
			}

			if response.Status != tt.expected.Status || response.Message != tt.expected.Message || !equalSlices(response.PolicyViolations, tt.expected.PolicyViolations) {
				t.Errorf("handler returned unexpected body: got %+v want %+v", response, tt.expected)
			}
		})
	}
}

func equalSlices(a, b []string) bool {
	if len(a) != len(b) {
		return false
	}
	for i := range a {
		if a[i] != b[i] {
			return false
		}
	}
	return true
}