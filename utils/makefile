-include .creds

BASEIMAGE := xycarto/terraform
IMAGE := $(BASEIMAGE):2023-04-19

profile := xycarto-admin
region := us-west-2

RUN ?= docker run -it --rm --net=host --privileged --user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE)

build:
	$(RUN) bash build-infra.sh

local-test: Dockerfile
	docker run -it --rm --net=host --privileged --user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE) \
	bash

docker-local: Dockerfile
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE)


