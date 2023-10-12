FROM postgres:11-bullseye

RUN apt-get update && apt-get install -y wget curl

ENV POSTGRES_PASSWORD=password-login-is-disabled

ARG uta_version=uta_20210129

MAINTAINER reecehart@gmail.com
ENV UTA_VERSION=${uta_version}
LABEL description="PostgreSQL image with $UTA_VERSION installed (https://github.com/biocommons/uta/)"

ADD load-uta.sh /docker-entrypoint-initdb.d/

# postgres entrypoint will run load-uta.sh automatically