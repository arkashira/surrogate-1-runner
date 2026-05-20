package main

import (
	"context"
	"fmt"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/cloudformation"
)

func CreateAWSEnvironment(stackName string, templateBody string) error {
	ctx := context.Background()
	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		return fmt.Errorf("failed to load AWS config: %w", err)
	}

	client := cloudformation.NewFromConfig(cfg)

	input := &cloudformation.CreateStackInput{
		StackName:   aws.String(stackName),
		TemplateBody: aws.String(templateBody),
	}

	start := time.Now()
	result, err := client.CreateStack(ctx, input)
	if err != nil {
		return fmt.Errorf("failed to create stack: %w", err)
	}

	fmt.Printf("Stack creation initiated: %v\n", result.StackId)

	// Wait for stack creation to complete
	waiter := cloudformation.NewStackCreateCompleteWaiter(client)
	err = waiter.Wait(ctx, &cloudformation.DescribeStacksInput{
		StackName: aws.String(stackName),
	}, 5*time.Minute)
	if err != nil {
		return fmt.Errorf("stack creation failed: %w", err)
	}

	elapsed := time.Since(start)
	fmt.Printf("Stack created successfully in %v\n", elapsed)

	return nil
}

func main() {
	stackName := "practice-environment"
	templateBody := `
	Resources:
	  ExampleResource:
	    Type: "AWS::S3::Bucket"
	`

	err := CreateAWSEnvironment(stackName, templateBody)
	if err != nil {
		fmt.Printf("Error creating AWS environment: %v\n", err)
		return
	}

	fmt.Println("AWS environment created successfully.")
}