variable "aws_region" {
  type        = string
  description = "AWS region for deployment"
}

variable "gcp_project" {
  type        = string
  description = "GCP project for deployment"
}

variable "gcp_region" {
  type        = string
  description = "GCP region for deployment"
}

variable "container_image" {
  type        = string
  description = "Container image for Freedom Link service"
}