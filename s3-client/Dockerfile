FROM asteurer/python_spin

ARG USER
ARG PASSWORD
ARG IMAGE_REPO
ARG IMAGE_TAG

WORKDIR /app
COPY main.py main.py
COPY requirements.txt requirements.txt
COPY spin.toml spin.toml

RUN pip install -r requirements.txt

RUN spin build

RUN spin registry login ${IMAGE_REPO} -u ${USER} -p ${PASSWORD}
RUN spin registry push ${IMAGE_REPO}/${IMAGE_TAG}