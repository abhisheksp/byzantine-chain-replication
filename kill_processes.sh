#!/usr/bin/env bash

echo 'Attempting to kill any running client and olympus nodes...'
kill $(ps aux | grep 'client.log' | awk '{print $2}')
kill $(ps aux | grep 'olympus.log' | awk '{print $2}')
kill $(ps aux | grep 'main.log' | awk '{print $2}')
