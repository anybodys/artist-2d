variable "app_versions" {
  type = map(string)
  default = {
    client : "0.2.0",
    api : "0.1.0.p1",
  }

}

variable "domain" {
  type    = string
  default = "kmdcodes.com"
}

variable "project" {
  type    = string
  default = "artist-2d"
}

variable "region" {
  type    = string
  default = "us-west1"
}

variable "ssl" {
  type    = bool
  default = true
}
