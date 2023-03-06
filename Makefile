DOCKER_IMAGE_NAME ?= opsdroid-slack-gke-k8s
DOCKER_IMAGE_TAG ?= latest

GCP_PROJECT ?= my-project
DOCKER_REGISTRY ?= gcr.io/$(GCP_PROJECT)

all: help

.PHONY: all help configure-docker

help:
	@echo "Targets:"
	@echo "  configure-docker       Sets docker credentials from gcloud. You must run this to set"
	@echo "                         the pullSecrets for kaniko"
	@echo ""
	@echo "  opsdroid               Run 'opsdroid start -f config.yaml' after loading '.myenv'"

opsdroid:
	set -aeu; . ./.myenv; opsdroid start -f config.yaml

configure-docker:
	gcloud auth configure-docker
