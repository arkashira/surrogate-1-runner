package firmware

import (
	"fmt"
)

// ValidateGPUCount checks if the GPU count is valid
func ValidateGPUCount(count int) error {
	if count < 2 {
		return fmt.Errorf("gpu count must be at least 2 for multi-gpu bridge")
	}
	return nil
}