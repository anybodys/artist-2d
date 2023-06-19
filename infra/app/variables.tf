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
    voting_api : "0.1.0",
    painter_api : "0.1.0",
  }

}
