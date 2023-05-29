provider "google" {
  project = var.project_name
  region  = var.region
}


# Create the Cloud Run service
resource "google_cloud_run_service" "voting_service" {
  name = "voting"
  location = var.region

  template {
    spec {
      containers {
        #us-west2-docker.pkg.dev/artist-2d/cloud-run-source-deploy/painter-api:latest
        image = "us-west2-docker.pkg.dev/artist-2d/cloud-run-source-deploy/voting-api:${var.app_versions["voting"]}"
        #gcr.io/google-samples/hello-app:1.0"
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }

}
