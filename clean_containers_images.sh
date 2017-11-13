#!/usr/bin/env bash

docker kill replicanode
docker rm replicanode
docker rmi replicanode_img