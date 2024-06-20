#!/bin/zsh

cd aks-cluster/terraform
terraform destroy --auto-approve
cd ../../s3-bucket/terraform
terraform destroy --auto-approve