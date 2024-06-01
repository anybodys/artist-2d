locals {
  api_domain = "api.${var.domain}"
}

resource "google_dns_managed_zone" "default" {
  name        = "kmdcodes-com"
  description = "DNS zone for domain: kmdcodes.com"
  dns_name    = "${var.domain}."
  labels = {
    "terraform" : true
  }

  dnssec_config {
    kind          = "dns#managedZoneDnsSecConfig"
    non_existence = "nsec3"
    state         = "on"

    default_key_specs {
      algorithm  = "rsasha256"
      key_length = 2048
      key_type   = "keySigning"
      kind       = "dns#dnsKeySpec"
    }
    default_key_specs {
      algorithm  = "rsasha256"
      key_length = 1024
      key_type   = "zoneSigning"
      kind       = "dns#dnsKeySpec"
    }
  }

  timeouts {}
}

resource "random_id" "tf_prefix" {
  byte_length = 4
}

resource "google_certificate_manager_dns_authorization" "default" {
  name        = "kmdcodes-dnsauth-${random_id.tf_prefix.hex}"
  description = "The default dns auth"
  domain      = var.domain
  labels = {
    "terraform" : true
  }
}

#resource "google_dns_record_set" "api_cname" {
#  name         = "${local.api_domain}."
#  managed_zone = google_dns_managed_zone.default.name
#  type         = "CNAME"
#  ttl          = 300
#  rrdatas = ["${var.domain}."]
#}

resource "google_dns_record_set" "a" {
  name         = google_dns_managed_zone.default.dns_name
  managed_zone = google_dns_managed_zone.default.name
  type         = "A"
  ttl          = 300
  rrdatas      = [module.lb-http.external_ip]
}

resource "google_dns_record_set" "api-a" {
  name         = "${local.api_domain}."
  managed_zone = google_dns_managed_zone.default.name
  type         = "A"
  ttl          = 300
  rrdatas      = [module.lb-http.external_ip]
}

data "google_compute_address" "external_ip" {
  name = "artist-address"
}

module "lb-http" {
  source  = "terraform-google-modules/lb-http/google//modules/serverless_negs"
  version = "~> 9.0"

  name    = "artist"
  project = var.project

  address                         = data.google_compute_address.external_ip.address
  ssl                             = var.ssl
  managed_ssl_certificate_domains = [var.domain, "${local.api_domain}"]
  https_redirect                  = var.ssl

  backends = {
    client = {
      description = "Frontend Client"
      groups = [
        {
          group = google_compute_region_network_endpoint_group.client_neg.id
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
    api = {
      description = "API Gateway"
      groups = [
        {
          group = google_compute_region_network_endpoint_group.api_neg.id
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

  create_url_map = false
  url_map        = google_compute_url_map.default.id
}

resource "google_compute_region_network_endpoint_group" "client_neg" {
  provider              = google-beta
  name                  = "client-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = data.google_cloud_run_service.client.name
  }
}

resource "google_compute_region_network_endpoint_group" "api_neg" {
  provider              = google-beta
  name                  = "api-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    url_mask = "api.${var.domain}/<service>"
  }
}

data "google_cloud_run_service" "client" {
  name     = "client"
  location = var.region
  project  = var.project
}

data "google_cloud_run_service" "votingapi" {
  name     = "votingapi"
  location = var.region
  project  = var.project
}

resource "google_cloud_run_domain_mapping" "client" {
  name     = var.domain
  location = data.google_cloud_run_service.client.location
  metadata {
    namespace = data.google_cloud_run_service.client.project
  }
  spec {
    route_name = data.google_cloud_run_service.client.name
  }
}

resource "google_cloud_run_service_iam_member" "public-access" {
  location = data.google_cloud_run_service.client.location
  project  = data.google_cloud_run_service.client.project
  service  = data.google_cloud_run_service.client.name
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_compute_url_map" "default" {
  name            = "http-lb"
  default_service = "artist-backend-client"

  host_rule {
    hosts        = [var.domain]
    path_matcher = "client"
  }

  host_rule {
    hosts        = [local.api_domain]
    path_matcher = "api"
  }

  path_matcher {
    name            = "client"
    default_service = "artist-backend-client"

  }

  path_matcher {
    name            = "api"
    default_service = "artist-backend-api"
  }
}
