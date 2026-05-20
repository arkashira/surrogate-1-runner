terraform {
  required_providers {
    workflow_automator = {
      source  = "axentx/workflow-automator"
      version = "~> 1.0"
    }
  }
}

provider "workflow_automator" {
  api_key = var.workflow_automator_api_key
  base_url = var.workflow_automator_base_url
}