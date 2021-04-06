#!/bin/bash

iptables -D INPUT -p tcp -m tcp --dport 53 -j DROP
iptables -D INPUT -p udp -m udp --dport 53 -j DROP