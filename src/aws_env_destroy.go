package main

import (
	"context"
	"fmt"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
)

func destroyAWSEnvironment() error {
	ctx := context.Background()
	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		return fmt.Errorf("failed to load AWS config: %w", err)
	}

	client := ec2.NewFromConfig(cfg)

	// List all instances
	input := &ec2.DescribeInstancesInput{}
	result, err := client.DescribeInstances(ctx, input)
	if err != nil {
		return fmt.Errorf("failed to describe instances: %w", err)
	}

	var instanceIDs []string
	for _, reservation := range result.Reservations {
		for _, instance := range reservation.Instances {
			instanceIDs = append(instanceIDs, *instance.InstanceId)
		}
	}

	if len(instanceIDs) == 0 {
		fmt.Println("No instances found.")
		return nil
	}

	// Terminate all instances
	terminateInput := &ec2.TerminateInstancesInput{
		InstanceIds: instanceIDs,
	}
	_, err = client.TerminateInstances(ctx, terminateInput)
	if err != nil {
		return fmt.Errorf("failed to terminate instances: %w", err)
	}

	fmt.Println("Instances termination initiated.")

	// Wait for instances to terminate
	waiter := ec2.NewInstanceTerminatedWaiter(client)
	waiterInput := &ec2.DescribeInstancesInput{
		InstanceIds: instanceIDs,
	}
	err = waiter.Wait(ctx, waiterInput, 300*time.Second)
	if err != nil {
		return fmt.Errorf("failed waiting for instances to terminate: %w", err)
	}

	fmt.Println("All instances terminated successfully.")
	return nil
}

func main() {
	err := destroyAWSEnvironment()
	if err != nil {
		fmt.Printf("Error destroying AWS environment: %v\n", err)
		return
	}
	fmt.Println("AWS environment destroyed successfully.")
}