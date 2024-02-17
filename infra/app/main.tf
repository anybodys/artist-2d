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
  client_tag    = var.app_versions["client"]
  client_image  = "${local.image_base}client:${local.client_tag}"
  painter_image = "${local.image_base}painter_api:${var.app_versions["painter_api"]}"
  voting_tag    = var.app_versions["voting_api"]
  voting_image  = "${local.image_base}voting_api:${local.voting_tag}"
}


# Create the Cloud Run service
resource "google_cloud_run_v2_service" "voting" {
  name     = "voting"
  location = var.region

  template {
    revision = "voting-${replace(local.voting_tag, ".", "-")}"
    containers {
      name  = "voting-api"
      image = local.voting_image
    }
  }
}

# Create the Cloud Run service
resource "google_cloud_run_v2_service" "client" {
  name     = "client"
  location = var.region

  template {
    revision = "client-${replace(local.client_tag, ".", "-")}"
    containers {
      name  = "client"
      image = local.client_image
      ports {
        container_port = 3000
      }
      startup_probe {
        initial_delay_seconds = 0
        period_seconds        = 3
        failure_threshold     = 1
        tcp_socket {
          port = 3000
        }
      }
    }
  }
}
