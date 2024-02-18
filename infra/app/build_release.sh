#!/bin/bash


echo `gcloud config get project`
echo `gcloud config get account`

gcloud auth configure-docker \
    us-west1-docker.pkg.dev -q > /dev/null|| exit 1

set +x

build_image () {
    app=$1
    image=$(terraform output -raw ${app}_image)
    echo "...checking if we need to build ${image}"
    docker pull ${image} > /dev/null 2>&1
    image_exists=$?
    if [ $image_exists -ne 0 ]; then
        echo "...image not found. We will build and push."
        docker build ../../${app}/ -t ${image} || exit 2
        docker push ${image} || exit 3
    fi
}

build_image voting_api
build_image painter_api
build_image client