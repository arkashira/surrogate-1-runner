package main

import (
	"context"
	"fmt"
	"time"

	"github.com/aws/aws-sdk-go-v2/aws"
	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/ec2"
)

func ListAWSEnvironments() ([]*ec2.Instance, error) {
	ctx := context.Background()
	cfg, err := config.LoadDefaultConfig(ctx)
	if err != nil {
		return nil, fmt.Errorf("failed to load AWS config: %w", err)
	}

	client := ec2.NewFromConfig(cfg)

	input := &ec2.DescribeInstancesInput{}
	startTime := time.Now()

	result, err := client.DescribeInstances(ctx, input)
	if err != nil {
		return nil, fmt.Errorf("failed to describe instances: %w", err)
	}

	elapsedTime := time.Since(startTime)
	if elapsedTime > 30*time.Second {
		return nil, fmt.Errorf("listing environments took longer than 30 seconds: %v", elapsedTime)
	}

	var instances []*ec2.Instance
	for _, reservation := range result.Reservations {
		instances = append(instances, reservation.Instances...)
	}

	return instances, nil
}

func main() {
	instances, err := ListAWSEnvironments()
	if err != nil {
		fmt.Printf("Error: %v\n", err)
		return
	}

	for _, instance := range instances {
		fmt.Printf("Instance ID: %s, State: %s\n", *instance.InstanceId, *instance.State.Name)
	}
}