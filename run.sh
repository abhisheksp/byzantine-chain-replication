#!/usr/bin/env bash

source compile.sh
python -m da -n MainNode --master  --message-buffer-size 1000000 main.da