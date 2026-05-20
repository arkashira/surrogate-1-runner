package services

import (
	"context"

	"github.com/axentx/surrogate/internal/types"
)

// PolicyService abstracts *any* source of policies (OPA, Guardrails, hard‑coded, DB, etc.).
type PolicyService interface {
	// ListPolicies returns all policy identifiers that the detector should evaluate.
	ListPolicies(ctx context.Context) ([]string, error)

	// EvaluatePolicy runs a single policy against the current cloud state and returns
	// zero or more violations.
	EvaluatePolicy(ctx context.Context, policyID string) ([]types.Violation, error)

	// The three AWS‑specific helpers are kept for the “quick‑start” implementation.
	EvaluateIAMUser(ctx context.Context, u *iam.User) []types.Violation
	EvaluateS3Bucket(ctx context.Context, b *s3.Bucket) []types.Violation
	EvaluateEC2Instance(ctx context.Context, i *ec2.Instance) []types.Violation
}