################################################################
## Voting API
################################################################

resource "google_service_account" "votingapi" {
  account_id   = "cloud-run-votingapi"
  display_name = "Service account for Cloud Run Voting API"
}

resource "google_cloud_run_v2_service" "votingapi" {
  name     = "votingapi"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {
    containers {
      name  = "votingapi"
      image = local.votingapi_image

      ports {
        container_port = 8000
      }

      env {
        name  = "ENV"
        value = "prod"
      }
      env {
        name  = "GOOGLE_CLOUD_PROJECT"
        value = var.project
      }
      env {
        name  = "STORAGEAPI_URL"
        value = google_cloud_run_v2_service.storageapi.uri
      }

    }
    service_account = google_service_account.votingapi.email
  }
}

# Allow unauthed requests.
resource "google_cloud_run_service_iam_binding" "votingapi" {
  location = google_cloud_run_v2_service.votingapi.location
  service  = google_cloud_run_v2_service.votingapi.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}
