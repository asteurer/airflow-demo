# Instructions

- Update your AWS credentials in /infra/aks-cluster/helm/airflow/values.yaml -> `airflow.extraEnv`
- Run the `/infra/build.sh` file
- Once this has finished, SSH/SFTP into the SFTP pod and add a file called `file.txt` with any text content.
