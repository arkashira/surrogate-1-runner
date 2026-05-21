package test

import (
	"testing"
	"net/http"
	"io/ioutil"
	"encoding/json"
)

type FreedomLinkResponse struct {
	Status string `json:"status"`
	Message string `json:"message"`
}

func TestFreedomLinkIntegration(t *testing.T) {
	url := "http://localhost:8080/freedom-link-endpoint"

	resp, err := http.Get(url)
	if err != nil {
		t.Fatalf("Failed to send request: %v", err)
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		t.Fatalf("Failed to read response body: %v", err)
	}

	var response FreedomLinkResponse
	err = json.Unmarshal(body, &response)
	if err != nil {
		t.Fatalf("Failed to unmarshal JSON: %v", err)
	}

	if response.Status != "success" {
		t.Errorf("Expected status 'success', got '%s'", response.Status)
	}

	if response.Message != "Access granted" {
		t.Errorf("Expected message 'Access granted', got '%s'", response.Message)
	}
}