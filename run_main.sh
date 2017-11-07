#!/usr/bin/env bash

source compile.sh
python -m da \
-n $NODE_NAME \
--master  \
--logfile \
--logfilename $LOG_PATH \
--logfilelevel $LOG_LEVEL \
--message-buffer-size $MESSAGE_BUFFER_SIZE \
main.da \
-c $CONFIG_FILE