#!/bin/bash

# bash build.sh

source .creds

git clone --branch terraform https://${TOKEN}@github.com/dragonfly-science/synth-chm.git

cp -r .creds synth-chm/src/geospatial/

cd synth-chm/src/geospatial/

echo ${DOCKER_PW} | sudo docker login --username deployhub1 --password-stdin

sudo make docker-pull

sudo make index-workunit

exit