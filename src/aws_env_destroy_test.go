package main

import (
	"context"
	"testing"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
)

func TestDestroyAWSEnvironment(t *testing.T) {
	ctx := context.Background()
	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		t.Fatalf("failed to load AWS config: %v", err)
	}

	client := ec2.NewFromConfig(cfg)

	// Create a test instance for testing purposes
	createInput := &ec2.RunInstancesInput{
		MinCount: aws.Int32(1),
		MaxCount: aws.Int32(1),
	}
	result, err := client.RunInstances(ctx, createInput)
	if err != nil {
		t.Fatalf("failed to create test instance: %v", err)
	}

	testInstanceID := *result.Instances[0].InstanceId

	// Call the function to destroy the environment
	err = destroyAWSEnvironment()
	if err != nil {
		t.Fatalf("failed to destroy AWS environment: %v", err)
	}

	// Check if the test instance is terminated
	waiter := ec2.NewInstanceTerminatedWaiter(client)
	waiterInput := &ec2.DescribeInstancesInput{
		InstanceIds: []string{testInstanceID},
	}
	err = waiter.Wait(ctx, waiterInput, 300*time.Second)
	if err != nil {
		t.Fatalf("failed waiting for test instance to terminate: %v", err)
	}

	t.Logf("Test instance %s terminated successfully.", testInstanceID)
}