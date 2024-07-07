################################################################
## Client
################################################################

resource "google_service_account" "client" {
  account_id   = "cloud-run-client"
  display_name = "Service account for Cloud Run Client"
}

resource "google_cloud_run_v2_service" "client" {
  name     = "client"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_ALL"

  template {

    containers {
      name  = "client"
      image = local.client_image

      ports {
        container_port = 3000
      }
    }

    service_account = google_service_account.client.email
  }
}

# Allow unauthed requests.
resource "google_cloud_run_service_iam_binding" "client" {
  location = google_cloud_run_v2_service.client.location
  service  = google_cloud_run_v2_service.client.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}


################################################################
## API
################################################################

resource "google_service_account" "api" {
  account_id   = "cloud-run-api"
  display_name = "Service account for Cloud Run API"
}

resource "google_cloud_run_v2_service" "api" {
  name     = "api"
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER"

  template {

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.artist2d.connection_name]
      }
    }

    containers {
      name  = "api"
      image = local.api_image

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
        name  = "POSTGRES_PORT"
        value = "5432"
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
        name  = "POSTGRES_DB"
        value = "artist"
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
      env {
        name = "GOOGLE_OAUTH2_KEY"
        value_source {
          secret_key_ref {
            secret  = "google-oauth-key"
            version = "latest"
          }
        }
      }
      env {
        name = "GOOGLE_OAUTH2_SECRET"
        value_source {
          secret_key_ref {
            secret  = "google-oauth-secret"
            version = "latest"
          }
        }
      }

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }
    }

    service_account = google_service_account.api.email
  }
}

# Allow unauthed requests.
resource "google_cloud_run_service_iam_binding" "api" {
  location = google_cloud_run_v2_service.api.location
  service  = google_cloud_run_v2_service.api.name
  role     = "roles/run.invoker"
  members = [
    "allUsers"
  ]
}

## Secrets and access.

resource "google_secret_manager_secret_iam_member" "storage-db-api" {
  secret_id = google_secret_manager_secret.storageapi-db-pass.id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.api.email}"
}

resource "google_secret_manager_secret" "api-secrets" {
  for_each  = toset(["google-oauth-key", "google-oauth-secret"])
  secret_id = each.key

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_iam_member" "api-secrets" {
  for_each  = google_secret_manager_secret.api-secrets
  secret_id = each.value.secret_id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.api.email}"
}

## DB things.

resource "google_project_iam_member" "cloudsql" {
  project = var.project
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.api.email}"
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
  member    = "serviceAccount:${google_service_account.api.email}"
}
