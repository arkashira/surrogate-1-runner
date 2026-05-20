# Introduction to Freedom Link Integration
The Freedom Link integration allows you to securely route AI requests without violating corporate firewall rules. This guide provides step-by-step instructions on how to configure the Freedom Link integration via Terraform modules.

## Prerequisites
Before you begin, ensure you have the following:
* Terraform installed on your machine
* An AWS or GCP account
* The Freedom Link Terraform module

## Step 1: Configure the Freedom Link Terraform Module
To configure the Freedom Link Terraform module, follow these steps:
1. Clone the Terraform module repository: `git clone https://github.com/axentx/freedom-link-terraform.git`
2. Navigate to the cloned repository: `cd freedom-link-terraform`
3. Initialize the Terraform working directory: `terraform init`
4. Apply the Terraform configuration: `terraform apply`

## Step 2: Deploy to AWS or GCP
To deploy the Freedom Link integration to AWS or GCP, follow these steps:
### AWS Deployment
1. Create an AWS provider file: `touch aws.tf`
2. Add the following code to the `aws.tf` file: