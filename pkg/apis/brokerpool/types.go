package brokerpool

import (
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

// BrokerPoolSpec defines the desired state of BrokerPool
type BrokerPoolSpec struct {
	// Brokers is a list of broker names that belong to this pool.
	Brokers []string `json:"brokers,omitempty"`
}

// BrokerPoolStatus defines the observed state of BrokerPool
type BrokerPoolStatus struct {
	// Ready indicates whether the pool has been fully reconciled.
	Ready bool `json:"ready,omitempty"`
}

// +kubebuilder:object:root=true
// +kubebuilder:subresource:status

// BrokerPool is the Schema for the brokerpools API
type BrokerPool struct {
	metav1.TypeMeta   `json:",inline"`
	metav1.ObjectMeta `json:"metadata,omitempty"`

	Spec   BrokerPoolSpec   `json:"spec,omitempty"`
	Status BrokerPoolStatus `json:"status,omitempty"`
}

// +kubebuilder:object:root=true

// BrokerPoolList contains a list of BrokerPool
type BrokerPoolList struct {
	metav1.TypeMeta `json:",inline"`
	metav1.ListMeta `json:"metadata,omitempty"`
	Items           []BrokerPool `json:"items"`
}