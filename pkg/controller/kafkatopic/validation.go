package kafkatopic

import (
	"context"
	"fmt"

	"github.com/axentx/axentx/pkg/kafka"
	"github.com/axentx/axentx/pkg/validation"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func validateBrokerPools(topic *KafkaTopic, clusterConfig *KafkaClusterConfig) error {
	existingPools, err := kafka.GetBrokerPools(context.Background(), clusterConfig.KafkaClusterName, clusterConfig.Namespace)
	if err != nil {
		return err
	}

	for _, pool := range topic.Spec.BrokerPools {
		if !contains(existingPools, pool) {
			return fmt.Errorf("broker pool '%s' does not exist in the cluster configuration", pool)
		}
	}

	return nil
}

func contains(slice []string, item string) bool {
	for _, a := range slice {
		if a == item {
			return true
		}
	}
	return false
}

// opt/axentx/surrogate-1/pkg/controller/kafkatopic/kafka_topic_controller.go
package kafkatopic

import (
	"context"
	"fmt"

	"github.com/axentx/axentx/pkg/validation"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"sigs.k8s.io/controller-runtime/pkg/client"
)

func (r *KafkaTopicReconciler) validate(topic *KafkaTopic) error {
	if err := validateBrokerPools(topic, r.clusterConfig); err != nil {
		return err
	}

	// Add other validation checks here...

	return nil
}

func (r *KafkaTopicReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	topic := &KafkaTopic{}
	if err := r.Get(ctx, req.NamespacedName, topic); err != nil {
		return ctrl.Result{}, client.IgnoreNotFound(err)
	}

	if err := r.validate(topic); err != nil {
		return ctrl.Result{}, fmt.Errorf("validation failed: %w", err)
	}

	// Proceed with topic creation/update...

	return ctrl.Result{}, nil
}