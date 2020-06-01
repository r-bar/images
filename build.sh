#!/bin/bash

IMAGE=$1
BASE_REPO=rbartech
REPO=$BASE_REPO/$IMAGE
TAGS=$(ls -1 $IMAGE/tags)

for TAG in $TAGS; do
  docker build $(cat $IMAGE/tags/$TAG) -t $REPO:$TAG $IMAGE
  docker push $REPO:$TAG
done
