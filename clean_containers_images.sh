#!/usr/bin/env bash

docker kill replicanode
docker kill replicanode1
docker rm replicanode
docker rm replicanode1
docker rmi replicanode_img