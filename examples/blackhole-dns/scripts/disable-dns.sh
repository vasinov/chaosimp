#!/bin/bash

# Original code by @adhorn
# from https://github.com/adhorn/chaos-ssm-documents/blob/master/run-command/experimental/blackhole-dns-stress.yml

iptables -A INPUT -p tcp -m tcp --dport 53 -j DROP
iptables -A INPUT -p udp -m udp --dport 53 -j DROP