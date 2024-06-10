################################################################
## Database server
################################################################

resource "random_password" "artist2d_db" {
  length  = 16
  special = false
}

resource "google_sql_database_instance" "artist2d" {
  name             = "artist2d"
  database_version = "POSTGRES_15"
  region           = var.region
  root_password    = random_password.artist2d_db.result

  settings {
    tier = "db-f1-micro"
  }

  deletion_protection = "false"
}

################################################################
## Logical Database -- the thing we connect to!
## And some user config
################################################################

resource "google_sql_database" "database" {
  name     = "artist"
  instance = google_sql_database_instance.artist2d.name
}


resource "random_password" "storageapi_db" {
  length  = 16
  special = false
}

resource "google_sql_user" "root" {
  name     = "postgres"
  instance = google_sql_database_instance.artist2d.name
  password = random_password.artist2d_db.result
}

resource "google_sql_user" "storageapi" {
  name     = "storageapi"
  instance = google_sql_database_instance.artist2d.name
  password = random_password.storageapi_db.result
}

resource "google_secret_manager_secret" "storageapi-db-pass" {
  secret_id = "storageapi-db-pass"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "storageapi-current" {
  secret = google_secret_manager_secret.storageapi-db-pass.id

  secret_data = random_password.storageapi_db.result
}

resource "postgresql_grant" "storageapi" {
  database    = google_sql_database.database.name
  role        = google_sql_user.storageapi.name
  schema      = "public"
  object_type = "database"
  privileges  = ["CONNECT", "CREATE", "TEMPORARY"]
}

provider "postgresql" {
  host            = google_sql_database_instance.artist2d.ip_address.0.ip_address
  port            = 5432
  database        = google_sql_database.database.name
  username        = google_sql_user.root.name
  password        = random_password.artist2d_db.result
  sslmode         = "require"
  connect_timeout = 15
}
