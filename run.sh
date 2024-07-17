#!/bin/bash
mkdir -p /docker/volume/tashmediatrans/media
docker container stop tashmediatrans
docker rm tashmediatrans
docker rmi tashmediatrans-image
docker build -t tashmediatrans-image .
docker run \
--name tashmediatrans \
-v /docker/volume/tashmediatrans/media:/home/app/webapp/media \
--net tashmediatrans-network \
-p 2001:2001 \
-d \
tashmediatrans-image