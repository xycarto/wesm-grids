#!/bin/bash

# bash run-index.sh "CA_SantaClaraCounty_2020"

source ../.creds

WORKUNIT=$1

git clone https://${TOKEN}@github.com/xycarto/wesm-grids.git

cp -r .creds wesm-grids/utils/src/

cd wesm-grids/utils/src

echo ${DOCKER_PW} | sudo docker login --username deployhub1 --password-stdin

sudo make docker-pull

sudo make wesm-index workunit=$WORKUNIT

exit