#!/usr/bin/env bash

source compile.sh
rm logs/replica.log
cd src
export IP_ADDR=`/sbin/ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'`
python -m da -D -n ReplicaNode --message-buffer-size 100000 --hostname $IP_ADDR --port $PORT main.da
