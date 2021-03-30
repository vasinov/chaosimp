#!/bin/bash

# based on https://github.com/adhorn/chaos-ssm-documents/blob/master/run-command/network-loss-stress.yml

if [[ "$( which tc 2>/dev/null )" ]] ; then echo Dependency is already installed. ; exit ; fi
echo "Installing required dependencies"
if [ -f  "/etc/system-release" ] ; then
  if cat /etc/system-release | grep -i 'Amazon Linux' ; then
    sudo amazon-linux-extras install testing
    sudo yum -y install tc
  else
    echo "There was a problem installing dependencies."
    exit 1
  fi
elif cat /etc/issue | grep -i Ubuntu ; then
  sudo apt-get update -y
  sudo DEBIAN_FRONTEND=noninteractive sudo apt-get install -y iproute2
else
  echo "There was a problem installing dependencies."
  exit 1
fi

MAX_FLAG_AGE_SECONDS=5
ATTEMPT_ROLLBACK_AT_SECONDS=10
STOP_TIME=$(( $(date +%s) + {{ Duration }} ))
RANDOM_STRING=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | head -c 32)
FLAG_PATH="/tmp/Run-Network-Packet-Drop-$RANDOM_STRING.flag"
ROLLBACK_COMMAND="tc qdisc del dev {{ Interface }} root netem loss {{ Loss }}% {{ Correlation }}%"
ROLLBACK_CHECK='if test ! -f "'$FLAG_PATH'" || test "$(( $(date +%s) - $(stat -c "%Y" '$FLAG_PATH') ))" -gt '$MAX_FLAG_AGE_SECONDS' ; then rm '$FLAG_PATH'; '$ROLLBACK_COMMAND' ; fi 2>/dev/null'
# this will enqueue a rollback check, after $ATTEMPT_ROLLBACK_AT_SECONDS seconds
schedule_rollback_attempt() {
  echo "sleep $ATTEMPT_ROLLBACK_AT_SECONDS; $ROLLBACK_CHECK" | at now
}
# this will delete the flag file, and rollback the fault injection
rollback() {
  rm $FLAG_PATH
  $ROLLBACK_COMMAND
  exit $?
}
# this will inject some packet drop on the network
inject_packet_drop() {
  echo "Injecting packet drop..."
  tc qdisc add dev {{ Interface }} root netem loss {{ Loss }}% {{ Correlation }}%
}
# binding the rollback function to these exit signals
trap rollback INT
trap rollback TERM
# atd must be running in order to use at later
atd || { echo Failed to run atd daemon, exiting... 1>&2 ; exit 1; }
schedule_rollback_attempt
inject_packet_drop
# for the duration of the injection, the flag file is updated, and a rollback check is enqueued
while [[ $(date +%s) -lt $STOP_TIME ]] ; do
  touch $FLAG_PATH
  schedule_rollback_attempt
  sleep $MAX_FLAG_AGE_SECONDS
done
# after the desired duration, the injection is removed
rollback
