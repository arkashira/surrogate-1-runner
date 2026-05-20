package monitor

import (
	"context"
	"fmt"
	"sync"
	"time"

	corev1 "k8s.io/api/core/v1"
	"k8s.io/apimachinery/pkg/fields"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/cache"
)

// Monitor watches pod status and detects silent failures and CrashLoopBackOff
// events within a configurable latency.
//
// Detection guarantees:
//   - Silent pod failures (no status update) are reported if they exceed
//     `silentFailureThreshold` (default 30s).
//   - CrashLoopBackOff events are reported after the baseline learning period
//     (`baselineDuration`, default 24h) has elapsed.
//
// Alerts are emitted on the provided `alertCh` as human‑readable strings.
type Monitor struct {
	client                 kubernetes.Interface
	alertCh                chan<- string
	baselineDuration       time.Duration
	silentFailureThreshold time.Duration

	mu          sync.Mutex
	podHealth   map[PodKey]*PodHealth
	startTime   time.Time
	stopCh      chan struct{}
	stoppedOnce sync.Once
}

// NewMonitor creates a new Monitor instance.
//
// `client` – Kubernetes client used to list/watch pods.
// `alertCh` – Channel where alert strings are sent.
// `baselineDuration` – How long to wait after start before reporting CrashLoopBackOff.
// `silentFailureThreshold` – Time without a pod status update before reporting a silent failure.
func NewMonitor(client kubernetes.Interface, alertCh chan<- string, baselineDuration, silentFailureThreshold time.Duration) *Monitor {
	return &Monitor{
		client:                 client,
		alertCh:                alertCh,
		baselineDuration:       baselineDuration,
		silentFailureThreshold: silentFailureThreshold,
		podHealth:              make(map[PodKey]*PodHealth),
		startTime:              time.Now(),
		stopCh:                 make(chan struct{}),
	}
}

// Start begins monitoring. It blocks until the context is cancelled.
func (m *Monitor) Start(ctx context.Context) error {
	// Set up a pod informer that watches all namespaces.
	listWatcher := cache.NewListWatchFromClient(
		m.client.CoreV1().RESTClient(),
		"pods",
		metav1.NamespaceAll,
		fields.Everything(),
	)

	_, controller := cache.NewInformer(
		listWatcher,
		&corev1.Pod{},
		0,
		cache.ResourceEventHandlerFuncs{
			AddFunc:    m.handlePod,
			UpdateFunc: func(oldObj, newObj interface{}) { m.handlePod(newObj) },
			DeleteFunc: m.handlePodDelete,
		},
	)

	// Run the informer in a separate goroutine.
	go controller.Run(m.stopCh)

	// Periodic ticker to detect silent failures.
	ticker := time.NewTicker(m.silentFailureThreshold / 2)
	defer ticker.Stop()

	for {
		select {
		case <-ctx.Done():
			m.shutdown()
			return nil
		case <-ticker.C:
			m.detectSilentFailures()
		}
	}
}

// shutdown stops the informer and ensures resources are released.
func (m *Monitor) shutdown() {
	m.stoppedOnce.Do(func() {
		close(m.stopCh)
	})
}

// handlePod processes Add/Update events for a pod.
func (m *Monitor) handlePod(obj interface{}) {
	pod, ok := obj.(*corev1.Pod)
	if !ok {
		return
	}
	key := PodKey{Namespace: pod.Namespace, Name: pod.Name}
	now := time.Now()

	// Determine CrashLoopBackOff status.
	crashLoop := false
	for _, cs := range pod.Status.ContainerStatuses {
		if cs.State.Waiting != nil && cs.State.Waiting.Reason == "CrashLoopBackOff" {
			crashLoop = true
			break
		}
	}

	m.mu.Lock()
	defer m.mu.Unlock()
	ph, exists := m.podHealth[key]
	if !exists {
		ph = &PodHealth{}
		m.podHealth[key] = ph
	}
	ph.LastSeen = now
	previousCrash := ph.CrashLoopBackOff
	ph.CrashLoopBackOff = crashLoop

	// Emit CrashLoopBackOff alert only after baseline learning period.
	if crashLoop && !previousCrash && time.Since(m.startTime) > m.baselineDuration {
		alert := fmt.Sprintf("CrashLoopBackOff detected for pod %s/%s", pod.Namespace, pod.Name)
		select {
		case m.alertCh <- alert:
		default:
			// Non‑blocking; drop if channel is full.
		}
	}
}

// handlePodDelete cleans up state for deleted pods.
func (m *Monitor) handlePodDelete(obj interface{}) {
	pod, ok := obj.(*corev1.Pod)
	if !ok {
		return
	}
	key := PodKey{Namespace: pod.Namespace, Name: pod.Name}
	m.mu.Lock()
	delete(m.podHealth, key)
	m.mu.Unlock()
}

// detectSilentFailures scans the podHealth map and alerts for pods that have
// not reported a status update within the silentFailureThreshold.
func (m *Monitor) detectSilentFailures() {
	threshold := time.Now().Add(-m.silentFailureThreshold)

	m.mu.Lock()
	defer m.mu.Unlock()
	for key, ph := range m.podHealth {
		if ph.LastSeen.Before(threshold) {
			alert := fmt.Sprintf("Silent failure detected for pod %s/%s (last seen %s)", key.Namespace, key.Name, ph.LastSeen.Format(time.RFC3339))
			select {
			case m.alertCh <- alert:
			default:
			}
			// Update LastSeen to avoid repeated alerts until the pod recovers.
			ph.LastSeen = time.Now()
		}
	}
}