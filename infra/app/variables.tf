variable "app_versions" {
  type = map(string)
  default = {
    client : "0.2.0",
    votingapi : "0.2.5",
    painterapi : "0.1.0",
    storageapi : "0.0.1",
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
