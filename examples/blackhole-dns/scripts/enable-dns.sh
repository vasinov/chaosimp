#!/bin/bash

# Original code by @adhorn
# from https://github.com/adhorn/chaos-ssm-documents/blob/master/run-command/experimental/blackhole-dns-stress.yml

echo 'iptables -D INPUT -p tcp -m tcp --dport 53 -j DROP' | at now + {{ Duration }} minutes
echo 'iptables -D INPUT -p udp -m udp --dport 53 -j DROP' | at now + {{ Duration }} minutes