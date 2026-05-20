provider "aws" {
  region = var.aws_region
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

resource "aws_api_gateway_rest_api" "freedom_link" {
  name        = "FreedomLinkAPI"
  description = "API for Freedom Link integration"
}

resource "google_cloud_run_service" "freedom_link" {
  name     = "freedom-link-service"
  location = var.gcp_region

  template {
    spec {
      containers {
        image = var.container_image
      }
    }
  }
}

resource "aws_api_gateway_resource" "freedom_link_resource" {
  rest_api_id = aws_api_gateway_rest_api.freedom_link.id
  parent_id   = aws_api_gateway_rest_api.freedom_link.root_resource_id
  path_part   = "freedom-link"
}

resource "aws_api_gateway_method" "freedom_link_method" {
  rest_api_id = aws_api_gateway_rest_api.freedom_link.id
  resource_id = aws_api_gateway_resource.freedom_link_resource.id
  http_method = "POST"
  authorization = "NONE"
}