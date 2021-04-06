#!/bin/bash

echo 'iptables -D INPUT -p tcp -m tcp --dport 53 -j DROP' | at now + {{ Duration }} minutes
echo 'iptables -D INPUT -p udp -m udp --dport 53 -j DROP' | at now + {{ Duration }} minutes