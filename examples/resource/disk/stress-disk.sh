#!/bin/bash

# Based on the code by @adhorn
# https://github.com/adhorn/chaos-ssm-documents/blob/master/run-command/diskspace-stress.yml

if [ {{ Duration }} -lt 1 ] || [ {{ Duration }} -gt 43200 ] ; then echo Duration parameter value must be between 1 and 43200 seconds && exit; fi

pgrep stress-ng && echo Another stress-ng command is running, exiting... && exit

echo Initiating Disk stress for {{ Duration }} seconds...

stress-ng --fallocate 1 --fallocate-bytes {{ Filesize }}g -t {{ Duration }}s

echo Finished Disk stress.