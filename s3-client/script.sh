#!/bin/zsh

op run --env-file=.env -- \
    sudo docker build . \
        --build-arg USER=$USER \
        --build-arg PASSWORD=$PASSWORD \
        --build-arg IMAGE_REPO=$IMAGE_REPO \
        --build-arg IMAGE_TAG=$IMAGE_TAG


# op run --env-file=.env -- \
#     spin up --from-registry index.docker.io/asteurer/airflow-s3-client