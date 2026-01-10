#!/bin/bash

PYTHONPATH="./" python3 ./input/main.py 300 4 & 
P1=$!
sleep 0.3
echo "=====run subcribers======="
PYTHONPATH="./" python3 ./output/main.py >> rabbit_300_4.csv 
P2=$!
