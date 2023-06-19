terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
}


provider "google" {
  project = var.project
  region  = var.region
}

data "google_client_config" "current" {
}

locals {
  image_base    = "${var.region}-docker.pkg.dev/${var.project}/${var.project}/"
  voting_image  = "${local.image_base}voting_api:${var.app_versions["voting_api"]}"
  painter_image = "${local.image_base}painter_api:${var.app_versions["painter_api"]}"
}


# Create the Cloud Run service
resource "google_cloud_run_service" "voting" {
  name     = "voting"
  location = var.region

  template {
    spec {
      containers {
        image = local.voting_image
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

}
