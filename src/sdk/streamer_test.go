package sdk

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestStreamer_Stream(t *testing.T) {
	testCases := []struct {
		name     string
		endpoint string
		payload  interface{}
		wantErr  bool
	}{
		{
			name:     "SuccessfulStream",
			endpoint: "http://localhost:8125",
			payload:  map[string]string{"key": "value"},
			wantErr:  false,
		},
		{
			name:     "FailedStream",
			endpoint: "http://localhost:8125",
			payload:  map[string]string{"key": "value"},
			wantErr:  true,
		},
	}

	for _, tc := range testCases {
		t.Run(tc.name, func(t *testing.T) {
			server := httptest.NewServer(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
				if tc.wantErr {
					w.WriteHeader(http.StatusInternalServerError)
					return
				}
				w.WriteHeader(http.StatusOK)
			}))
			defer server.Close()

			s := NewStreamer(server.URL)
			err := s.Stream(tc.payload)

			if tc.wantErr {
				assert.Error(t, err)
			} else {
				assert.NoError(t, err)
			}
		})
	}
}