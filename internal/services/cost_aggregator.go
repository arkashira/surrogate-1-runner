package internal

import (
	"context"
	"fmt"
	"log"
	"time"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/ec2"
	"github.com/aws/aws-sdk-go/service/resourcegroups"
	"github.com/google/uuid"

	"axentx/surrogate-1/internal/config"
	"axentx/surrogate-1/internal/models"
)

type CostAggregator struct {
	cfg *config.Config
}

func NewCostAggregator(cfg *config.Config) *CostAggregator {
	return &CostAggregator{cfg: cfg}
}

func (ca *CostAggregator) Aggregate(ctx context.Context, start, end time.Time) (*models.CostBreakdown, error) {
	sess, err := session.NewSession(&aws.Config{Region: aws.String(ca.cfg.Region)}, nil)
	if err != nil {
		return nil, err
	}

	ec2Svc := ec2.New(sess)
	rgrpSvc := resourcegroups.New(sess)

	costBreakdown := models.NewCostBreakdown()

	// AWS
	awsCost, err := ca.aggregateAWS(ctx, ec2Svc, rgrpSvc, start, end)
	if err != nil {
		return nil, err
	}
	costBreakdown.AWS = awsCost

	// GCP
	gcpCost, err := ca.aggregateGCP(ctx, start, end)
	if err != nil {
		return nil, err
	}
	costBreakdown.GCP = gcpCost

	// Azure
	azureCost, err := ca.aggregateAzure(ctx, start, end)
	if err != nil {
		return nil, err
	}
	costBreakdown.Azure = azureCost

	return costBreakdown, nil
}

func (ca *CostAggregator) aggregateAWS(ctx context.Context, ec2Svc *ec2.EC2, rgrpSvc *resourcegroups.ResourceGroups, start, end time.Time) (*models.ServiceCost, error) {
	// TODO: implement AWS aggregation logic
	return nil, fmt.Errorf("AWS aggregation not implemented")
}

func (ca *CostAggregator) aggregateGCP(ctx context.Context, start, end time.Time) (*models.ServiceCost, error) {
	// TODO: implement GCP aggregation logic
	return nil, fmt.Errorf("GCP aggregation not implemented")
}

func (ca *CostAggregator) aggregateAzure(ctx context.Context, start, end time.Time) (*models.ServiceCost, error) {
	// TODO: implement Azure aggregation logic
	return nil, fmt.Errorf("Azure aggregation not implemented")
}