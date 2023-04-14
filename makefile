-include .creds

BASEIMAGE := xycarto/wesm-grids
IMAGE := $(BASEIMAGE):2023-04-14

RUN ?= docker run -it --rm  \
	-e POSTGRES_HOST_AUTH_METHOD=trust \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE)

# Make tiler docker

wesm-index:
	$(RUN) python3 utils/build-index.py

local-edit: Dockerfile
	docker run -it --rm  \
	-e POSTGRES_HOST_AUTH_METHOD=trust \
	-e DISPLAY=$$DISPLAY \
	--env-file .creds \
	-e RUN= -v$$(pwd):/work \
	-w /work $(IMAGE)
	bash
	
local: Dockerfile
	docker build --tag $(BASEIMAGE) - < $<  && \
	docker tag $(BASEIMAGE) $(IMAGE)

