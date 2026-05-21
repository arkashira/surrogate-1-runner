package main

import (
	"testing"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/forecast"
)

func TestForecastFutureCosts(t *testing.T) {
	awsSession, err := session.NewSession(&aws.Config{Region: aws.String("us-west-2")}, nil)
	if err != nil {
		t.Fatal(err)
	}

	bt := NewBudgetingTools(awsSession)

	ctx := context.Background()

	resourceId := "arn:aws:forecast:us-west-2:123456789012:forecast/METERED"

	prediction, err := bt.ForecastFutureCosts(ctx, resourceId)
	if err != nil {
		t.Fatal(err)
	}

	if prediction == nil {
		t.Errorf("prediction is nil")
	}
}

func TestSetBudget(t *testing.T) {
	awsSession, err := session.NewSession(&aws.Config{Region: aws.String("us-west-2")}, nil)
	if err != nil {
		t.Fatal(err)
	}

	bt := NewBudgetingTools(awsSession)

	ctx := context.Background()

	resourceId := "arn:aws:forecast:us-west-2:123456789012:forecast/METERED"

	err = bt.SetBudget(ctx, resourceId, 100.0)
	if err != nil {
		t.Fatal(err)
	}
}