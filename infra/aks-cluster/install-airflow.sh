#!/bin/zsh

kubectl create namespace airflow
kubectl get namespaces

helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm search repo airflow
helm install airflow apache-airflow/airflow --namespace airflow --debug

sleep 30

kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow

# This saves the apachd-airflow helm template locally
# helm show values apache-airflow/airflow > helm/values.yaml

# This is for accessing the repo for gitSync via SSH. Currently, the only way gitSync will work is if the repo is public and is being accessed via HTTP. 
# kubectl create secret generic airflow-ssh-git-secret --from-file=gitSshKey=/home/andyboi/.ssh/github -n airflow

# This upgrades the helm install to the changes made in the helm/values.yaml file
# helm upgrade --install airflow apache-airflow/airflow -n airflow -f helm/values.yaml --debug