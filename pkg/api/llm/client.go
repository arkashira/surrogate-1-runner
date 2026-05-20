package llm

import (
	"net/http"
	"bytes"
	"encoding/json"
	"io/ioutil"
	"path/to/signature" // Assuming the signature package is in this path
)

// Client represents an LLM client
type Client struct {
	BaseURL    string
	HTTPClient *http.Client
}

// NewClient creates a new LLM client
func NewClient(baseURL string) *Client {
	return &Client{
		BaseURL:    baseURL,
		HTTPClient: &http.Client{},
	}
}

// CallLLM calls the LLM endpoint with the given request
func (c *Client) CallLLM(req *http.Request) (*http.Response, error) {
	// Mask the request signature
	maskedRequest, err := signature.MaskRequest(req)
	if err != nil {
		return nil, err
	}

	// Set the masked signature in the request header
	req.Header.Set("X-Masked-Signature", maskedRequest.MaskedSignature)

	// Make the HTTP request
	resp, err := c.HTTPClient.Do(req)
	if err != nil {
		return nil, err
	}

	return resp, nil
}