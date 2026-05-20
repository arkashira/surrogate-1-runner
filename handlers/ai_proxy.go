
package handlers

import (
	"net/http"
	"net/http/httputil"
	"net/url"
	"time"

	"github.com/axentx/surrogate-1/config"
	"github.com/axentx/surrogate-1/proxies"
)

func aiProxyHandler(w http.ResponseWriter, r *http.Request) {
	// Use a randomized User-Agent string
	r.Header.Set("User-Agent", config.RandomUserAgent())

	// Rotate IP addresses via a pool of proxies
	proxy, err := proxies.Get()
	if err != nil {
		http.Error(w, "Error getting proxy", http.StatusInternalServerError)
		return
	}
	defer proxies.Return(proxy)

	// Send traffic over HTTPS with TLS 1.3
	transport := &http.Transport{
		TLSClientConfig: &tls.Config{MinVersion: tls.VersionTLS13},
	}
	client := &http.Client{Transport: transport}

	// Include a custom header to avoid signature detection
	r.Header.Set("X-Custom-Header", "AvoidSignatureDetection")

	// Dial the target URL using the proxy
	targetURL, err := url.Parse(proxy.URL)
	if err != nil {
		http.Error(w, "Error parsing proxy URL", http.StatusInternalServerError)
		return
	}
	targetURL.Host = r.URL.Host
	targetURL.Path = r.URL.Path
	newReq := *r
	newReq.URL = targetURL
	newReq.Transport = transport
	newReq.Host = targetURL.Host

	// Tunnel the request through the proxy
	resp, err := http.DefaultTransport.RoundTrip(httputil.NewSingleHostReverseProxy(targetURL))
	if err != nil {
		http.Error(w, "Error tunneling request", http.StatusInternalServerError)
		return
	}

	// Copy the response headers
	for k, v := range resp.Header {
		for _, vv := range v {
			w.Header().Add(k, vv)
		}
	}

	// Write the response body
	_, err = io.Copy(w, resp.Body)
	if err != nil {
		http.Error(w, "Error writing response", http.StatusInternalServerError)
		return
	}
}