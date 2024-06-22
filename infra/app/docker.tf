locals {
  docker_hostname = "${var.region}-docker.pkg.dev"
  image_root      = "${local.docker_hostname}/${var.project}/${var.project}"
}

provider "docker" {
  registry_auth {
    address = local.docker_hostname
  }
}


resource "docker_image" "app" {
  for_each = var.app_versions
  name     = "${local.image_root}/${each.key}"

  build {
    # The application's directory.
    context = "${path.cwd}/../../${each.key}"
    tag     = ["${local.image_root}/${each.key}:${each.value}"]
  }

  triggers = {
    # Trigger a build if this value has changed.
    version_tag = each.value
  }
}

resource "docker_registry_image" "app" {
  for_each      = docker_image.app
  name          = tolist(docker_image.app[each.key].build)[0].tag[0]
  keep_remotely = true
}
