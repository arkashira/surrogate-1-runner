package k8s

import (
	"context"
	"time"

	"github.com/prometheus/client_golang/prometheus"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/rest"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/apimachinery/pkg/api/errors"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/runtime/schema"
	"k8s.io/client-go/util/retry"
)

var (
	podRestarts = prometheus.NewCounterVec(
		prometheus.CounterOpts{
			Name: "axentx_pod_restarts_total",
			Help: "Total number of pod restarts initiated",
		},
		[]string{"namespace", "pod_name"},
	)
	podRestartLatency = prometheus.NewHistogramVec(
		prometheus.HistogramOpts{
			Name:    "axentx_pod_restart_latency_seconds",
			Help:    "Time taken to restart pods",
			Buckets: prometheus.DefBuckets,
		},
		[]string{"namespace", "pod_name"},
	)
)

func init() {
	prometheus.MustRegister(podRestarts)
	prometheus.MustRegister(podRestartLatency)
}

type Client struct {
	kubeClient kubernetes.Interface
}

func NewClient(kubeconfig string) (*Client, error) {
	var config *rest.Config
	var err error

	if kubeconfig != "" {
		config, err = clientcmd.BuildConfigFromFlags("", kubeconfig)
	} else {
		config, err = rest.InClusterConfig()
	}
	if err != nil {
		return nil, err
	}

	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		return nil, err
	}

	return &Client{kubeClient: clientset}, nil
}

func (c *Client) RestartPod(namespace, name string) error {
	start := time.Now()

	ctx := context.TODO()
	err := retry.RetryOnConflict(retry.DefaultRetry, func() error {
		pod, err := c.kubeClient.CoreV1().Pods(namespace).Get(ctx, name, metav1.GetOptions{})
		if err != nil {
			return err
		}

		// Force delete to trigger restart
		propagation := metav1.DeletePropagationForeground
		return c.kubeClient.CoreV1().Pods(namespace).Delete(
			ctx,
			name,
			metav1.DeleteOptions{
				PropagationPolicy: &propagation,
				GracePeriodSeconds: func() *int64 { 
					v := int64(0)
					return &v 
				}(),
			},
		)
	})

	latency := time.Since(start).Seconds()
	podRestartLatency.WithLabelValues(namespace, name).Observe(latency)
	if err == nil {
		podRestarts.WithLabelValues(namespace, name).Inc()
	} else {
		prometheus.MustRegister(podRestartFailures.WithLabelValues(namespace, name))
	}

	return err
}

func (c *Client) WatchPodStatus(namespace, name string) (PodHealth, error) {
	ctx := context.TODO()
	pod, err := c.kubeClient.CoreV1().Pods(namespace).Get(ctx, name, metav1.GetOptions{})
	if err != nil {
		return PodHealth{}, err
	}

	return PodHealth{
		Namespace: namespace,
		Name:      name,
		Status:    string(pod.Status.Phase),
		RestartedAt: time.Now(),
	}, nil
}