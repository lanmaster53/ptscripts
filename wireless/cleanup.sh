#!/bin/bash
set -o verbose
killall airbase-ng
service dhcp3-server stop
killall python
ifconfig mitm down
brctl delbr mitm
iptables --flush
iptables --table nat --flush
iptables --delete-chain
iptables --table nat --delete-chain
echo '0' > /proc/sys/net/ipv4/ip_forward
airmon-ng stop mon0 &> /dev/null
route del -net 192.168.3.0 netmask 255.255.255.0 gw 192.168.3.1
ifconfig
route -n
iptables -nvL -t nat
