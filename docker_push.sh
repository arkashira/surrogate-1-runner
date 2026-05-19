#!/bin/bash

# Push the image to the internal registry with a semantic version tag
docker tag surrogate-1:latest surrogate-1:$(git rev-parse --short HEAD)
docker push surrogate-1:$(git rev-parse --short HEAD)