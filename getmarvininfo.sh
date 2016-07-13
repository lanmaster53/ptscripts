#!/bin/bash

# set variables
SWINT=eth2
BRINT=br0
COMPINT=eth3
ARPS=50 # if needed
TCP=445 # if needed

ifconfig $COMPINT 0.0.0.0 up promisc
echo [!] Plug in $COMPINT
tcpdump -i $COMPINT -nne -l -s0 -c1 port 67 | tee boot.capture
COMPMAC=`cat boot.capture | awk '{ print $2}' | head -1`
ifconfig $COMPINT down
macchanger -m $COMPMAC $SWINT

echo [*] Building interface bridge...
brctl addbr $BRINT
brctl addif $BRINT $COMPINT
brctl addif $BRINT $SWINT

echo [*] Bringing up interfaces...
ifconfig $COMPINT 0.0.0.0 up promisc
ifconfig $SWINT 0.0.0.0 up promisc
ifconfig $BRINT 0.0.0.0 up promisc

# sleeping to let things settle a tad
echo [*] Sleeping...
sleep 5

mii-tool -r $COMPINT
mii-tool -r $SWINT

echo [*] Getting info from traffic...
# get variables using arp
echo [!] Plug in $SWINT
tcpdump -i $SWINT -nne -l -s0 -c$ARPS arp | tee boot.capture
echo [*] Done receiving traffic. Processing...
GWMAC=`cat boot.capture | grep 'is-at' | awk '{ print $2 "," $4  $11 "," $13}' | sort | uniq -c | sort -rn | head -1 | awk -F ',' '{print $4}'`
GWIP=`cat boot.capture | grep 'is-at' | awk '{ print $2 "," $4  $11 "," $13}' | sort | uniq -c | sort -rn | head -1 | awk -F ',' '{print $3}'`
#COMPMAC=`cat boot.capture | grep 'is-at' | awk '{ print $2 "," $4  $11 "," $13}' | sort | uniq -c | sort -rn | head -1 | awk -F ',' '{print $2}'`
COMPIP=`cat boot.capture | grep $COMPMAC | grep -w "$GWIP tell"| head -1 | awk '{print $14}' | cut -d, -f 1`

# grab a single tcp packet destined for the DC (kerberos, smb, etc.)
#tcpdump -i $COMPINT -nne -l -s0 -c1 tcp dst port $TCP | tee boot.capture
#echo [*] Done receiving traffic. Processing...
#COMPMAC=`cat boot.capture | awk '{print $2}'`
#COMPIP=`cat boot.capture | awk '{print $10}' | cut -d. -f 1-4`
#GWMAC=`cat boot.capture | awk '{print $4}' | cut -d, -f 1`
#GWIP=`cat boot.capture | awk '{print $12}' | cut -d. -f 1-4`

echo [*] Bringing down bridge...
ifconfig $BRINT down
brctl delif $BRINT $COMPINT
brctl delif $BRINT $SWINT
ifconfig $BRINT 0.0.0.0 up promisc

MACr=aa:bb:cc:dd:ee:ff
IPr=10.0.0.1
BRNM=255.255.255.0

echo
echo =============================
echo Marvin Settings
echo =============================
echo BRIF1.INTERFACE: $COMPINT
echo BRIF2.INTERFACE: $SWINT
echo TAPIF.INTERFACE: $BRINT
echo =============================
echo MACr: $MACr
echo IPr: $IPr
echo =============================
echo BRIF1.SMAC: $GWMAC
echo BRIF1.SADDR: $GWIP
echo =============================
echo BRIF2.SMAC: $COMPMAC
echo BRIF2.SADDR: $COMPIP
echo =============================
echo BR.GATEWAY: $GWIP
echo BR.NETMASK: $BRNM
echo =============================
echo

echo [*] Building marvin.conf file...
rm marvin.conf
echo brif1.interface=$COMPINT >> marvin.conf
echo brif1.smac=$GWMAC >> marvin.conf
echo brif1.saddr=$GWIP >> marvin.conf
echo brif2.interface=$SWINT >> marvin.conf
echo brif2.smac=$COMPMAC >> marvin.conf
echo brif2.saddr=$COMPIP >> marvin.conf
echo br.netmask=$BRNM >> marvin.conf
echo br.gateway=$GWIP >> marvin.conf
echo tapif.interface=$BRINT >> marvin.conf
echo tapif.MACr=$MACr >> marvin.conf
echo tapif.IPr=$IPr >> marvin.conf

echo
echo 1. Validate br.netmask
echo 2. Configure tap client with:
echo address: 10.0.0.2
echo netmask: 255.255.255.0
echo gateway: 10.0.0.1
echo 3. Run marvin with \'./marvin.sh -f marvin.conf\' # modify marvin.sh to fix arguments
