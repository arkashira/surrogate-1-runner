package services

import (
	"context"

	"github.com/axentx/surrogate/internal/types"
)

// RemediationService knows how to fix a violation (run a Lambda, call Terraform, etc.).
type RemediationService interface {
	Remediate(ctx context.Context, v types.Violation) error
}