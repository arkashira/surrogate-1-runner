terraform {
  required_providers {
    surrogate = {
      source = "axentx/surrogate"
      version = "0.1.0"
    }
  }
}

provider "surrogate" {}

resource "surrogate_workflow" "example" {
  name    = "daily_ingest"
  steps   = ["fetch", "normalize", "dedupe", "upload"]
  enabled = true
}