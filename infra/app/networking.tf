module "lb-http" {
  source  = "terraform-google-modules/lb-http/google//modules/serverless_negs"
  version = "~> 9.0"

  name    = "artist"
  project = var.project

  ssl                             = var.ssl
  managed_ssl_certificate_domains = [var.domain]
  https_redirect                  = var.ssl

  backends = {
    default = {
      description = null
      groups = [
        {
          group = google_compute_region_network_endpoint_group.serverless_neg.id
        }
      ]
      enable_cdn = false

      iap_config = {
        enable = false
      }
      log_config = {
        enable = false
      }
    }
  }
}

resource "google_compute_region_network_endpoint_group" "serverless_neg" {
  provider              = google-beta
  name                  = "serverless-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = data.google_cloud_run_service.client.name
  }
}


data "google_cloud_run_service" "client" {
  name     = "client"
  location = var.region
  project  = var.project
}

resource "google_cloud_run_service_iam_member" "public-access" {
  location = data.google_cloud_run_service.client.location
  project  = data.google_cloud_run_service.client.project
  service  = data.google_cloud_run_service.client.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}
