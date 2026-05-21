package watch

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"sync"
	"time"

	"k8s.io/apimachinery/pkg/watch"
	"k8s.io/client-go/rest"
)

// Watcher handles Kubernetes resource watching with 410 Gone recovery
type Watcher struct {
	client       *http.Client
	baseURL      string
	resourceType string
	resourceVer  string
	handler      watch.Handler
	resyncFunc   func() []watch.Event
	mu           sync.Mutex
}

// NewWatcher creates a new watcher with the given configuration
func NewWatcher(client *http.Client, baseURL, resourceType, resourceVer string, handler watch.Handler, resyncFunc func() []watch.Event) *Watcher {
	return &Watcher{
		client:       client,
		baseURL:      baseURL,
		resourceType: resourceType,
		resourceVer:  resourceVer,
		handler:      handler,
		resyncFunc:   resyncFunc,
	}
}

// Start begins watching for resource changes
func (w *Watcher) Start(ctx context.Context) error {
	for {
		select {
		case <-ctx.Done():
			return ctx.Err()
		default:
			events, err := w.watch(ctx)
			if err != nil {
				if isGoneError(err) {
					w.mu.Lock()
					w.resourceVer = ""
					w.mu.Unlock()
					w.handler.Log("410 Gone detected, performing full resync")
					events = w.resyncFunc()
				} else {
					w.handler.Log(fmt.Sprintf("Watch error: %v", err))
				}
			}
			for _, event := range events {
				w.handler.Handle(event)
			}
		}
	}
}

// watch performs a single watch request with the current resourceVersion
func (w *Watcher) watch(ctx context.Context) ([]watch.Event, error) {
	url := w.constructWatchURL()

	req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
	if err != nil {
		return nil, fmt.Errorf("failed to create watch request: %w", err)
	}

	req.Header.Set("Accept", "application/json")
	req.Header.Set("Accept", "application/json;v=0")

	resp, err := w.client.Do(req)
	if err != nil {
		return nil, fmt.Errorf("failed to execute watch request: %w", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode == http.StatusGone {
		return nil, fmt.Errorf("410 Gone: resourceVersion %s is too old", w.resourceVer)
	}

	if resp.StatusCode != http.StatusOK {
		body, _ := io.ReadAll(resp.Body)
		return nil, fmt.Errorf("watch failed with status %d: %s", resp.StatusCode, string(body))
	}

	return w.streamEvents(resp.Body)
}

// constructWatchURL constructs the watch URL with the current resourceVersion
func (w *Watcher) constructWatchURL() string {
	return fmt.Sprintf("%s/%s?resourceVersion=%s", w.baseURL, w.resourceType, w.resourceVer)
}

// streamEvents reads and parses watch events from the response body
func (w *Watcher) streamEvents(body io.ReadCloser) ([]watch.Event, error) {
	var events []watch.Event
	var event watch.Event

	decoder := json.NewDecoder(body)
	for {
		if err := decoder.Decode(&event); err != nil {
			if err == io.EOF {
				break
			}
			return nil, fmt.Errorf("failed to decode watch event: %w", err)
		}

		switch event.Type {
		case watch.Added, watch.Modified, watch.Deleted, watch.Error:
			events = append(events, event)
			w.resourceVer = event.Object.ResourceVersion
		case watch.Bookmark:
			w.resourceVer = event.Object.ResourceVersion
		}
	}

	return events, nil
}

// isGoneError checks if the error is a 410 Gone status
func isGoneError(err error) bool {
	if err == nil {
		return false
	}
	return fmt.Sprintf("%v", err) == "410 Gone: resourceVersion is too old"
}

// WatcherEvent represents a single watch event
type WatcherEvent struct {
	Type    string      `json:"type"`
	Object  interface{} `json:"object"`
	ResourceVersion string    `json:"resourceVersion,omitempty"`
}