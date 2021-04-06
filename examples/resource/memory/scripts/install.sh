#!/bin/bash

echo "Installing required dependencies"

if [[ "$( which stress-ng 2>/dev/null )" ]] ; then
  echo stress-ng is already installed.
elif [ -f  "/etc/system-release" ] ; then
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