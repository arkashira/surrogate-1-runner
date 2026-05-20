package kafkatopic

// BrokerPoolMapping defines partition-to-broker-pool assignments
type BrokerPoolMapping map[int32]string

// GetBrokerPoolForPartition returns the broker pool for a given partition
// Returns empty string if no explicit mapping exists
func (m BrokerPoolMapping) GetBrokerPoolForPartition(partition int32) string {
	return m[partition]
}

// ValidateMapping checks if the mapping is consistent with topic configuration
func (m BrokerPoolMapping) Validate(numPartitions int32, validPools []string) error {
	var errs []string

	for p, pool := range m {
		if p < 0 || p >= numPartitions {
			errs = append(errs, fmt.Sprintf("partition %d exceeds partition count %d", p, numPartitions))
		}
		if !contains(validPools, pool) {
			errs = append(errs, fmt.Sprintf("partition %d references invalid pool %q", p, pool))
		}
	}

	if len(errs) > 0 {
		return fmt.Errorf("invalid partition mapping: %s", strings.Join(errs, "; "))
	}
	return nil
}