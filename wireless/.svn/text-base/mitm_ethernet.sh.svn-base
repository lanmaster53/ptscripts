#!/bin/bash

echo "PRE-REQUISITES"
echo "=============="
echo "- External interface configured and communicating."
echo "- Connection between internal interface <-> WAP LAN port. WAP must have DHCP DISABLED."
echo " "

LOGDIR="$(date +%F-%H%M)"
mkdir $LOGDIR
cd $LOGDIR

# get var from user
ifconfig | grep 'Link\|addr'
echo -n "Enter the name of the internal interface: "
read -e IFACE

# set up interfaces, routing and iptables
ifconfig $IFACE down
ifconfig $IFACE 192.168.3.1 netmask 255.255.255.0 up
echo "1" > /proc/sys/net/ipv4/ip_forward
route add -net 192.168.3.0 netmask 255.255.255.0 gw 192.168.3.1
iptables -t nat -A POSTROUTING -j MASQUERADE
#firefox http://root:lime5463@192.168.3.2:8080/DHCPTable.htm &

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
dhcpd3 -q -cf dhcpd.conf -pf /var/run/dhcp3-server/dhcpd.pid $IFACE &
echo "Launching DMESG"
xterm -bg black -fg red -T "System Logs" -e tail -f /var/log/messages &

# ettercap notes
# must re-enable ip forwarding (echo "1" > ...) after ettercap starts
#ettercap -T -q -p -l ettercap.log -i $IFACE // // &
#echo "1" > /proc/sys/net/ipv4/ip_forward

# burp notes
# disable "loopback only" and enable "invisible proxy"
#iptables -A PREROUTING -t nat -s 192.168.3.2 -p tcp -m multiport --dport 80,443 -j DNAT --to 192.168.3.1:8080

echo "Done."
