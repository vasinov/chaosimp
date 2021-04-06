#!/bin/bash

# Based on the code by @adhorn
# https://github.com/adhorn/chaos-ssm-documents/blob/master/run-command/memory-stress.yml

if [ {{ Duration }} -lt 1 ] || [ {{ Duration }} -gt 43200 ] ; then echo Duration parameter value must be between 1 and 43200 seconds && exit; fi

pgrep stress-ng && echo Another stress-ng command is running, exiting... && exit

echo Initiating memory stress for {{ Duration }} seconds, 1 worker, using {{ Percent }} of total available memory...

stress-ng --vm 1 --vm-bytes {{ Percent }}% -t {{ Duration }}s

echo Finished memory stress.