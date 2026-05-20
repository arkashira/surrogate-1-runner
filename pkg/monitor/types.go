package monitor

import "time"

// PodKey uniquely identifies a pod in the cluster.
type PodKey struct {
	Namespace string
	Name      string
}

// PodHealth captures the last observed state of a pod relevant for health
// monitoring.
type PodHealth struct {
	// LastSeen is the timestamp of the most recent event for this pod.
	LastSeen time.Time

	// CrashLoopBackOff indicates whether the pod is currently in a
	// CrashLoopBackOff state.
	CrashLoopBackOff bool
}