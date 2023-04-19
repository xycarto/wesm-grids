-include .creds

BASEIMAGE := xycarto/terraform
IMAGE := $(BASEIMAGE):2023-04-19

profile := df
region := us-east-1

local-test: Dockerfile
	docker run -it --rm --net=host --user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE) \
	bash

docker-local: Dockerfile
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE)


