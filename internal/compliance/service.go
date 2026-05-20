package compliance

import (
	"context"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	s3types "github.com/aws/aws-sdk-go-v2/service/s3/types"
	"github.com/aws/aws-sdk-go-v2/service/s3"
	"github.com/aws/aws-sdk-go-v2/service/iam"
	"github.com/aws/aws-sdk-go-v2/service/cloudtrail"
	"github.com/aws/aws-sdk-go-v2/service/s3control"
)

// AWSClients groups the services we need.  In production we instantiate the real clients;
// in tests we replace them with mocks.
type AWSClients struct {
	S3          *s3.Client
	IAM         *iam.Client
	CloudTrail  *cloudtrail.Client
	S3Control   *s3control.Client
}

// NewAWSClients creates a client set using the default credential chain and the region
// supplied via the AWS_REGION env var (or us-east-1 as fallback).
func NewAWSClients(ctx context.Context) (*AWSClients, error) {
	cfg, err := config.LoadDefaultConfig(ctx,
		config.WithRegion(os.Getenv("AWS_REGION")),
	)
	if err != nil {
		return nil, err
	}
	return &AWSClients{
		S3:         s3.NewFromConfig(cfg),
		IAM:        iam.NewFromConfig(cfg),
		CloudTrail: cloudtrail.NewFromConfig(cfg),
		S3Control:  s3control.NewFromConfig(cfg),
	}, nil
}