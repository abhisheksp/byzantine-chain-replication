#!/usr/bin/env bash

source compile.sh
python -m da -n MainNode --master  --logfile --logfilename ../logs/main.log --logfilelevel info --message-buffer-size 1000000 main.da -c stress_1000_7_10.txt