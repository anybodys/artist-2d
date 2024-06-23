terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "3.0.2"
    }
    google = {
      source  = "hashicorp/google"
      version = "5.32.0"
    }
    #postgresql = {
    #  source  = "cyrilgdn/postgresql"
    #  version = "1.22.0"
    #}
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
  storageapi_image = docker_registry_image.app["storageapi"].name
  votingapi_image  = docker_registry_image.app["votingapi"].name
}
