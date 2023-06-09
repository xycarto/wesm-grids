#!/bin/bash

## Example for single run
# bash build-infra.sh "CA_SantaClaraCounty_2020" "California"

WORKUNIT=$1
STATE=$2

source .creds

cp -r terraform terraform-${WORKUNIT}

cd terraform-${WORKUNIT}

terraform init 

terraform apply -auto-approve

terraform validate

# Add instance description and test here
aws ec2 wait instance-status-ok --region "us-west-2" --instance-ids $(terraform output -raw instance_id) 

scp -o StrictHostKeyChecking=no -i ${key} -r ../.creds ubuntu@$(terraform output -raw instance_public_ip):/home/ubuntu/

scp -o StrictHostKeyChecking=no -i ${key}  -r ../run-index.sh ubuntu@$(terraform output -raw instance_public_ip):/home/ubuntu/

ssh -o StrictHostKeyChecking=no -i ${key}  ubuntu@$(terraform output -raw instance_public_ip) "bash run-index.sh $WORKUNIT $STATE"

terraform destroy -auto-approve

cd ../

rm -rf terraform-${WORKUNIT}