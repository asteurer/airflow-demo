#!/bin/zsh



# Creating and accessing the Azure infrastructure
cd aks-cluster/terraform
terraform apply --auto-approve && terraform output -json > outputs.json
RESOURCE_GROUP=$(jq -r '.resource_group.value' outputs.json)
AKS_CLUSTER=$(jq -r '.aks_cluster.value' outputs.json)
az login && az aks get-credentials --resource-group $RESOURCE_GROUP --name $AKS_CLUSTER --admin

# Creating the AWS infrastructure
cd ../../s3-bucket/terraform
terraform apply --auto-approve

cd ../..

SPIN_NAMESPACE = spin-apps
FTP_NAMESPACE = ftp-server

kubectl create namespace airflow
kubectl create namespace "$FTP_NAMESPACE"
kubectl create namespace "$SPIN_NAMESPACE"

./install-spinkube.sh "$SPIN_NAMESPACE"

helm install ftp-server ./aks-cluster/helm/ftp-server -n "$FTP_NAMESPACE"
helm install s3-app ./aks-cluster/helm/spin -n "$SPIN_NAMESPACE"
helm install airflow apache-airflow/airflow -n airflow -f aks-cluster/helm/airflow/values.yaml --debug

sleep 30
kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow

# The below code is how to install the default apache airflow helm template:
# helm repo add apache-airflow https://airflow.apache.org
# helm repo update
# helm search repo airflow
# helm install airflow apache-airflow/airflow --namespace airflow --debug