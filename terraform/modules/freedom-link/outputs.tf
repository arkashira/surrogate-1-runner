output "aws_api_gateway_id" {
  value       = aws_api_gateway_rest_api.freedom_link.id
  description = "ID of the AWS API Gateway"
}

output "gcp_cloud_run_service_name" {
  value       = google_cloud_run_service.freedom_link.name
  description = "Name of the GCP Cloud Run service"
}