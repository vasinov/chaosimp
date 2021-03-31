#!/bin/bash

echo Starting to stress all CPUs for 60 seconds...
stress-ng --cpu 0 --cpu-method matrixprod -t 60s
echo Finished stressing CPUs