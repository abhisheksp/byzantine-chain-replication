#!/usr/bin/env bash

source compile.sh
python -m da -n MainNode --master  --logfile --logfilename ../logs/main.log --logfilelevel info --message-buffer-size 100000 main.da -c order_proof_verification.txt
