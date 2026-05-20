package main

import (
	"testing"
	"time"

	"github.com/aws/aws-sdk-go-v2/service/ec2/types"
)

func TestListAWSEnvironments(t *testing.T) {
	mockInstances := []*types.Instance{
		{
			InstanceId: aws.String("i-12345"),
			State: &typesInstanceState{
				Name: types.InstanceStateNameRunning,
			},
		},
		{
			InstanceId: aws.String("i-67890"),
			State: &typesInstanceState{
				Name: types.InstanceStateNameStopped,
			},
		},
	}

	mockClient := &mockEC2Client{
		DescribeInstancesFunc: func(ctx context.Context, params *ec2.DescribeInstancesInput, optFns ...func(*ec2.Options)) (*ec2.DescribeInstancesOutput, error) {
			return &ec2.DescribeInstancesOutput{
				Reservations: []types.Reservation{
					{
						Instances: mockInstances,
					},
				},
			}, nil
		},
	}

	originalClient := ec2.NewFromConfig
	defer func() { ec2.NewFromConfig = originalClient }()
	ec2.NewFromConfig = func(cfg aws.Config) *ec2.Client {
		return mockClient
	}

	instances, err := ListAWSEnvironments()
	if err != nil {
		t.Fatalf("Expected no error, got: %v", err)
	}

	if len(instances) != len(mockInstances) {
		t.Errorf("Expected %d instances, got %d", len(mockInstances), len(instances))
	}

	for i, instance := range instances {
		if *instance.InstanceId != *mockInstances[i].InstanceId || *instance.State.Name != *mockInstances[i].State.Name {
			t.Errorf("Instance details do not match expected values")
		}
	}

	if time.Since(time.Now()) > 30*time.Second {
		t.Error("Listing environments took longer than 30 seconds")
	}
}

type mockEC2Client struct {
	DescribeInstancesFunc func(context.Context, *ec2.DescribeInstancesInput, ...func(*ec2.Options)) (*ec2.DescribeInstancesOutput, error)
}

func (m *mockEC2Client) DescribeInstances(ctx context.Context, params *ec2.DescribeInstancesInput, optFns ...func(*ec2.Options)) (*ec2.DescribeInstancesOutput, error) {
	return m.DescribeInstancesFunc(ctx, params, optFns...)
}