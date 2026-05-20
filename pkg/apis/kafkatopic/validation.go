package kafkatopic

import (
	"fmt"
	"sort"
	"strings"
)

// ValidateKafkaTopic checks invariants for KafkaTopic objects
func ValidateKafkaTopic(topic *KafkaTopic, validBrokerPools []string) error {
	var errs []string

	// Validate partition-broker-pool mapping
	if len(topic.Spec.PartitionBrokerPools) > 0 {
		// Check that all referenced pools exist
		for partition, pool := range topic.Spec.PartitionBrokerPools {
			if !contains(validBrokerPools, pool) {
				errs = append(errs, fmt.Sprintf("partition %d references non-existent broker pool %q", partition, pool))
			}
		}

		// Check that all partition numbers are valid
		for partition := range topic.Spec.PartitionBrokerPools {
			if partition < 0 || partition >= int(topic.Spec.NumPartitions) {
				errs = append(errs, fmt.Sprintf("partition %d exceeds topic's partition count %d", partition, topic.Spec.NumPartitions))
			}
		}
	}

	if len(errs) > 0 {
		return fmt.Errorf("invalid KafkaTopic spec: %s", strings.Join(errs, "; "))
	}
	return nil
}

func contains(haystack []string, needle string) bool {
	sort.Strings(haystack)
	i := sort.SearchStrings(haystack, needle)
	return i < len(haystack) && haystack[i] == needle
}