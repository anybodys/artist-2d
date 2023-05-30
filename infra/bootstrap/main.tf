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
