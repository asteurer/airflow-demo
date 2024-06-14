kubectl create namespace airflow
kubectl get namespaces

helm repo add apache-airflow https://airflow.apache.org
helm repo update
helm search repo airflow
helm install airflow apache-airflow/airflow --namespace airflow --debug

kubectl port-forward svc/airflow-webserver 8080:8080 -n airflow

helm show values apache-airflow/airflow > values.yaml

kubectl create secret generic airflow-ssh-git-secret --from-file=gitSshKey=/your/path/.ssh/id_rsa -n airflow

helm upgrade --install airflow apache-airflow/airflow -n airflow -f values.yaml --debug