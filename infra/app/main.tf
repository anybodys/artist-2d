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

