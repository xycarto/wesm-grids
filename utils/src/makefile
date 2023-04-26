include ../.creds

DOCKER_PW := ${DOCKER_PW}

BASEIMAGE := xycarto/wesm-grids
IMAGE := $(BASEIMAGE):2023-04-21

RUN ?= docker run --rm  \
	-e POSTGRES_HOST_AUTH_METHOD=trust \
	-e DISPLAY=$$DISPLAY \
	--env-file ../.creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE)

# Make tiler docker

wesm-index:
	$(RUN) python3 build-index.py $(workunit)

local-edit: Dockerfile
	docker run -it --rm  \
	-e POSTGRES_HOST_AUTH_METHOD=trust \
	-e DISPLAY=$$DISPLAY \
	--env-file ../.creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE)
	bash
	
docker-local: Dockerfile
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE)

docker: Dockerfile
	echo $(DOCKER_PW) | docker login --username xycarto --password-stdin
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE) && \
	docker push $(IMAGE)

docker-pull:
	docker pull $(IMAGE)