#!/bin/bash

# bash run-index.sh

source .creds

git clone https://${TOKEN}@github.com/xycarto/wesm-grids.git

cp -r .creds wesm-grids/utils/src/

cd wesm-grids/utils/src

sudo make docker-local

sudo make wesm-index workunit="CA_SantaClaraCounty_2020"

exit