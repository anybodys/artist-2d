variable "project" {
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
    client : "0.1.0",
    voting_api : "0.1.1",
    painter_api : "0.1.0",
  }

}
