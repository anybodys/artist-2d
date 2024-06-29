locals {
  api_domain = "api.${var.domain}"
}

# TODO: This should be built in Terraform.
data "google_cloud_run_service" "client" {
  name     = "client"
  location = var.region
  project  = var.project
}

resource "google_compute_region_network_endpoint_group" "client_neg" {
  name                  = "client-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = data.google_cloud_run_service.client.name
  }
}

resource "google_compute_region_network_endpoint_group" "votingapi_neg" {
  name                  = "votingapi-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    service = google_cloud_run_v2_service.votingapi.name
  }
}

resource "google_compute_region_network_endpoint_group" "internalapi_neg" {
  name                  = "internalapi-neg"
  network_endpoint_type = "SERVERLESS"
  region                = var.region
  cloud_run {
    #url_mask = "<service>"
    service = google_cloud_run_v2_service.storageapi.name
  }
}


################################################################
## External
################################################################

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

data "google_compute_global_address" "external_ip" {
  name = "artist-address"
}

module "lb-http" {
  source  = "terraform-google-modules/lb-http/google//modules/serverless_negs"
  version = "~> 9.0"

  name    = "artist"
  project = var.project

  address                         = data.google_compute_global_address.external_ip.address
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
    votingapi = {
      description = "External API"
      groups = [
        {
          group = google_compute_region_network_endpoint_group.votingapi_neg.id
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
    default_service = "artist-backend-votingapi"
  }
}

################################################################
## Internal
################################################################

resource "google_compute_network" "ilb_network" {
  provider = google-beta

  name = "l7-ilb-network"

  # We want custom subnets.
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "proxy" {
  provider = google-beta

  name          = "l7-ilb-proxy-subnet"
  ip_cidr_range = "10.0.0.0/24"
  purpose       = "REGIONAL_MANAGED_PROXY"
  region        = var.region
  role          = "ACTIVE"
  network       = google_compute_network.ilb_network.id
}

resource "google_compute_subnetwork" "ilb" {
  provider = google-beta

  name          = "l7-ilb-subnet"
  ip_cidr_range = "10.0.1.0/24"
  region        = var.region
  network       = google_compute_network.ilb_network.id
}

resource "google_compute_address" "ilb" {
  name         = "l7-ilb-address"
  subnetwork   = google_compute_subnetwork.ilb.id
  address_type = "INTERNAL"
  region       = var.region
}

resource "google_compute_forwarding_rule" "ilb" {
  name                  = "l7-ilb-forwarding-rule"
  region                = var.region
  depends_on            = [google_compute_subnetwork.proxy]
  ip_protocol           = "TCP"
  ip_address            = google_compute_address.ilb.address
  load_balancing_scheme = "INTERNAL_MANAGED"
  port_range            = "80"
  target                = google_compute_region_target_http_proxy.ilb.id
  network               = google_compute_network.ilb_network.id
  subnetwork            = google_compute_subnetwork.ilb.id
  network_tier          = "PREMIUM"
}

resource "google_compute_region_target_http_proxy" "ilb" {
  name    = "l7-ilb-target-http-proxy"
  region  = google_compute_region_backend_service.internalapi.region
  url_map = google_compute_region_url_map.ilb.id
}

resource "google_compute_region_url_map" "ilb" {
  name            = "l7-ilb-regional-url-map"
  region          = google_compute_region_backend_service.internalapi.region
  default_service = google_compute_region_backend_service.internalapi.id
}

resource "google_compute_region_backend_service" "internalapi" {
  name                  = "internalapi"
  region                = var.region
  load_balancing_scheme = "INTERNAL_MANAGED"

  backend {
    group          = google_compute_region_network_endpoint_group.internalapi_neg.self_link
    balancing_mode = "UTILIZATION"
  }
}
