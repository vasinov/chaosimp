#!/bin/bash

# Based on the code by @adhorn
# https://github.com/adhorn/chaos-ssm-documents/blob/master/run-command/io-stress.yml

if [ {{ Duration }} -lt 1 ] || [ {{ Duration }} -gt 43200 ] ; then echo Duration parameter value must be between 1 and 43200 seconds && exit; fi

pgrep stress-ng && echo Another stress-ng command is running, exiting... && exit

echo Initiating IO stress for {{ Duration }} seconds...

stress-ng --iomix 1 --iomix-bytes {{ Percent }}% -t {{ Duration }}s

echo Finished IO stress.