package main

import (
	"context"
	"fmt"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/cloudformation"
)

func DestroyAWSEnvironment(stackName string) error {
	ctx := context.Background()
	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		return fmt.Errorf("failed to load AWS config: %w", err)
	}

	client := cloudformation.NewFromConfig(cfg)

	input := &cloudformation.DeleteStackInput{
		StackName: aws.String(stackName),
	}

	result, err := client.DeleteStack(ctx, input)
	if err != nil {
		return fmt.Errorf("failed to delete stack: %w", err)
	}

	fmt.Printf("Stack deletion initiated: %v\n", result.StackId)

	// Wait for stack deletion to complete
	waiter := cloudformation.NewStackDeleteCompleteWaiter(client)
	err = waiter.Wait(ctx, &cloudformation.DescribeStacksInput{
		StackName: aws.String(stackName),
	}, 5*time.Minute)
	if err != nil {
		return fmt.Errorf("stack deletion failed: %w", err)
	}

	fmt.Println("Stack deleted successfully.")

	return nil
}

func main() {
	stackName := "practice-environment"

	err := DestroyAWSEnvironment(stackName)
	if err != nil {
		fmt.Printf("Error destroying AWS environment: %v\n", err)
		return
	}

	fmt.Println("AWS environment destroyed successfully.")
}