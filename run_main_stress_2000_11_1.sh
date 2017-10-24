#!/usr/bin/env bash

source compile.sh
python -m da -n MainNode --master  --logfile --logfilename ../logs/main.log --logfilelevel info --message-buffer-size 100000000 main.da -c stress_2000_11_1.txt