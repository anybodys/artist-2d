terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
  }
  backend "gcs" {
    bucket = "artist-2d-bucket-tfstate-dev"
    prefix = "terraform/state"
  }
}


provider "google" {
  project = var.project
  region  = var.region
}

provider "google-beta" {
  project = var.project
}

data "google_client_config" "current" {
}

locals {
  image_base    = "${var.region}-docker.pkg.dev/${var.project}/${var.project}/"
  client_tag    = var.app_versions["client"]
  client_image  = "${local.image_base}client:${local.client_tag}"
  painter_image = "${local.image_base}painterapi:${var.app_versions["painterapi"]}"
  voting_tag    = var.app_versions["votingapi"]
  voting_image  = "${local.image_base}votingapi:${local.voting_tag}"
}
