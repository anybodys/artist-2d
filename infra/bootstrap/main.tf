provider "google" {
  project = var.project_name
  region  = var.region
}


resource "google_artifact_registry_repository" "image_repo" {
  location      = var.region
  repository_id = var.project_name
  description   = "Arist 2D Docker Images"
  format        = "DOCKER"
}

resource "google_storage_bucket" "terraform_state" {
  name          = "artist-2d-bucket-tfstate-dev"
  force_destroy = false
  location      = "US"
  storage_class = "STANDARD"
  versioning {
    enabled = true
  }
}

terraform {
  required_version = "~> 1.4"

  required_providers {
    google = "~> 4.66"
  }
}
