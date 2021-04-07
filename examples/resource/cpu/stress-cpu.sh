#!/bin/bash

# Based on the code by @adhorn
# from https://github.com/adhorn/chaos-ssm-documents/blob/master/run-command/cpu-stress.yml

if [ {{ Duration }} -lt 1 ] || [ {{ Duration }} -gt 43200 ] ; then echo Duration parameter value must be between 1 and 43200 seconds && exit; fi

pgrep stress-ng && echo Another stress-ng command is running, exiting... && exit

echo Initiating CPU stress for {{ Duration }} seconds...

stress-ng --cpu 0 --cpu-method matrixprod --cpu-load {{ Load }} -t {{ Duration }}s

echo Finished CPU stress.