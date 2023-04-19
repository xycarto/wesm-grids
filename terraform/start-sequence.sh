#!/bin/bash

source .creds

git clone https://${TOKEN}@github.com/dragonfly-science/synth-chm.git

cp -r .creds synth-chm/src/geospatial/

echo ${PWD} 

cd synth-chm/src/geospatial 

tmux new -d -s workunit

tmux send-keys -t workunit.0 "echo ${DOCKER_PW} | sudo docker login --username deployhub1 --password-stdin" ENTER

sleep 10

tmux send-keys -t workunit.0 "sudo make docker-pull" ENTER

sleep 100

tmux send-keys -t workunit.0 "sudo make workunit" ENTER

# make workunit
