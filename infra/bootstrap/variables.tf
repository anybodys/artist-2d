variable "project_name" {
  type    = string
  default = "artist-2d"
}

variable "region" {
  type    = string
  default = "us-west1"
}

variable "app_versions" {
  type = map(string)
  default = {
    voting : "v0.1.0",
    painter : "v0.1.0",
  }
}
