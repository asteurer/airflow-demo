# Airflow Test

Airflow test repository.

## Installation

Remember to use docker compose V2. 

```bash
mkdir -p ./logs ./plugins ./config
docker compose up
```

The first time you run the command, it will take a while to run the Airflow initialization.

You can log in to the Airflow UI at [http://localhost:8080](http://localhost:8080) with the username `airflow` and the password `airflow`.

The SFTP server is available at [localhost:22](localhost:22) with the username `demo` and the password `demo`. You can use the `sftp` command to connect to the server.

```bash
sftp demo@localhost
```
