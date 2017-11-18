#!/usr/bin/env bash

docker rm replicanode0  -f
docker rm replicanode1  -f
docker rm replicanode2  -f
docker rm replicanode3  -f
docker rm replicanode4  -f
docker rm replicanode5  -f
docker rmi replicanode_img