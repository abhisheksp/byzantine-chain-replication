#!/usr/bin/env bash

echo "Deleting old log file: $LOG_FILE_PATH"
rm $LOG_FILE_PATH
echo 'Compiling DistAlgo files...'
source compile.sh
export IP_ADDR=`/sbin/ifconfig eth0 | grep 'inet addr' | cut -d: -f2 | awk '{print $1}'`
python -m da -D -n ReplicaNode --message-buffer-size 100000 --hostname $IP_ADDR --port $PORT --logfile --logfilename $LOG_FILE_PATH --logfilelevel $LOG_LEVEL main.da
