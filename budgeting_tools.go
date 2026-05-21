package main

import (
	"context"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/forecast"
)

type BudgetingTools struct {
	awsSession *session.Session
	forecast   *forecast.Forecast
}

func NewBudgetingTools(awsSession *session.Session) *BudgetingTools {
	return &BudgetingTools{
		awsSession: awsSession,
		forecast:   forecast.New(awsSession),
	}
}

func (bt *BudgetingTools) ForecastFutureCosts(ctx context.Context, resourceId string) (*forecast.Prediction, error) {
	input := &forecast.GetForecastInput{
		ForecastArn: aws.String(resourceId),
	}

	output, err := bt.forecast.GetForecastWithContext(ctx, input)
	if err != nil {
		return nil, err
	}

	return output.Prediction, nil
}

func (bt *BudgetingTools) SetBudget(ctx context.Context, resourceId string, budget float64) error {
	input := &forecast.UpdateForecastInput{
		ForecastArn: aws.String(resourceId),
		ForecastTypes: []*forecast.ForecastType{
			{
				ForecastType: aws.String("METERED"),
				Forecast: &forecast.Forecast{
					Items: []*forecast.Item{
						{
							Value: aws.Float64(budget),
						},
					},
				},
			},
		},
	}

	_, err := bt.forecast.UpdateForecastWithContext(ctx, input)
	if err != nil {
		return err
	}

	return nil
}

func main() {
	awsSession, err := session.NewSession(&aws.Config{Region: aws.String("us-west-2")}, nil)
	if err != nil {
		log.Fatal(err)
	}

	bt := NewBudgetingTools(awsSession)

	ctx := context.Background()

	resourceId := "arn:aws:forecast:us-west-2:123456789012:forecast/METERED"

	prediction, err := bt.ForecastFutureCosts(ctx, resourceId)
	if err != nil {
		log.Fatal(err)
	}

	fmt.Println(prediction)

	err = bt.SetBudget(ctx, resourceId, 100.0)
	if err != nil {
		log.Fatal(err)
	}
}