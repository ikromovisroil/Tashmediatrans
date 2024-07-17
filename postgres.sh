#!/bin/bash
mkdir -p /home/docker/volume/postgres
docker container stop postgres || true && docker rm postgres || true
docker rmi postgres-image || true
docker build -t postgres-image -f Dockerfile.postgres .
docker run \
--name postgres  \
--net tashmediatrans-network \
-v /home/docker/volume/postgres:/var/lib/postgresql/data \
-p 5432:5432 \
-d \
postgres-image