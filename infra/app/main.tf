terraform {
  required_providers {
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
  image_base     = "${var.region}-docker.pkg.dev/${var.project}/${var.project}/"
  client_tag     = var.app_versions["client"]
  voting_tag     = var.app_versions["votingapi"]
  storageapi_tag = var.app_versions["storageapi"]
}

################################################################
## Storage API
################################################################

resource "google_service_account" "storageapi" {
  account_id   = "cloud-run-service-account"
  display_name = "Service account for Cloud Run Storage API"
}

resource "google_cloud_run_v2_service" "storageapi" {
  name     = "storageapi"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_ONLY"

  template {

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.artist2d.connection_name]
      }
    }

    containers {
      image = "${local.image_base}storageapi:${local.storageapi_tag}"

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
        name  = "POSTGRES_HOST"
        value = "/cloudsql/${var.project}:${var.region}:${google_sql_database_instance.artist2d.name}"
      }
      env {
        name = "SECRET_KEY"
        value_source {
          secret_key_ref {
            secret  = "django-secret-key"
            version = "latest"
          }
        }
      }
      env {
        name  = "POSTGRES_USER"
        value = "storageapi"
      }
      env {
        name = "POSTGRES_PASSWORD"
        value_source {
          secret_key_ref {
            secret  = "storageapi-db-pass"
            version = "latest"
          }
        }
      }
      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
    }
    service_account = google_service_account.storageapi.email
  }
}

resource "google_secret_manager_secret_iam_member" "storage-db-api" {
  secret_id = google_secret_manager_secret.storageapi-db-pass.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.storageapi.email}"
}

resource "google_project_iam_member" "cloudsql" {
  project = var.project
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.storageapi.email}"
}

## Django Secret Key secret.

resource "random_password" "django-secret-key" {
  length = 64
}

resource "google_secret_manager_secret" "django-secret-key" {
  secret_id = "django-secret-key"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "django-secret-current" {
  secret = google_secret_manager_secret.django-secret-key.id

  secret_data = random_password.django-secret-key.result
}

resource "google_secret_manager_secret_iam_member" "django-secret-key" {
  secret_id = google_secret_manager_secret.django-secret-key.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.storageapi.email}"
}
