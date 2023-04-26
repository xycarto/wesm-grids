-include .creds

BASEIMAGE := xycarto/terraform
IMAGE := $(BASEIMAGE):2023-04-19

RUN ?= docker run --rm --net=host --privileged --user=$$(id -u):$$(id -g) \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE)

# run like "make build workunit="CA_SantaClaraCounty_2020""
build:
	$(RUN) bash build-infra.sh $(workunit)

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


