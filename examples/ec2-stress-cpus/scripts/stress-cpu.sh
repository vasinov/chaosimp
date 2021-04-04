#!/bin/bash

# Original code by @adhorn
# from https://github.com/adhorn/chaos-ssm-documents/blob/master/run-command/cpu-stress.yml

if [[ "$( which stress-ng 2>/dev/null )" ]] ; then echo Dependency is already installed. ; exit ; fi

echo "Installing required dependencies"

if [ -f  "/etc/system-release" ] ; then
  if cat /etc/system-release | grep -i 'Amazon Linux' ; then
    sudo amazon-linux-extras install testing
    sudo yum -y install stress-ng
  else
    echo "There was a problem installing dependencies."
    exit 1
  fi
elif cat /etc/issue | grep -i Ubuntu ; then
  sudo apt-get update -y
  sudo DEBIAN_FRONTEND=noninteractive sudo apt-get install -y stress-ng
else
  echo "There was a problem installing dependencies."
  exit 1
fi

echo Starting to stress all CPUs for 60 seconds...

stress-ng --cpu 0 --cpu-method matrixprod -t 60s

echo Finished stressing CPUs