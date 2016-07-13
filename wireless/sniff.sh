#!/bin/bash
#
# sniff.sh
# A simple script that allows your Mac to perform packet sniffing on
# unencrypted WiFi networks.
# ----------
# Usage:
#     ./sniff.sh (keyword)
#
# `keyword` is optional and is simply appended to the resulting
#           packetdump filename. You can use this as a reminder of
#           where you created this packet dump. (i.e.,
#           "sniff.sh starbucks")
# ----------
# Copyright (c) 2010, Mike Tigas
# http://mike.tig.as/
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


# On my MacBook Pro, the WiFi (AirPort) card is en1. Change accordingly.
WIFICARD="en1"

# Get our IP address & MAC. 
IP_ADDR=`ifconfig $WIFICARD | grep "inet " |awk '{print $2}'`
ETHER_ADDR=`ifconfig $WIFICARD | grep "ether " |awk '{print $2}'`

if [ -z $IP_ADDR ]; then
    echo "ifconfig could not obtain your IP address."
    echo "Are you using the correct interface (currently $WIFICARD) and is AirPort turned on?"
    exit 1
fi
if [ -z $ETHER_ADDR ]; then
    echo "ifconfig could not obtain your MAC address."
    echo "Are you using the correct interface (currently $WIFICARD) and is AirPort turned on?"
    exit 1
fi

# The first argument (if given) is a keyword/nickname that we tack onto the filename.
# I use this so I can remember where I was when I sniffed packets.
if [ -n $1 ]; then
    OUTPUT_FILE=~/Desktop/`date +"%Y%m%d-%H%M%S"`_$1.pcap
else
    OUTPUT_FILE=~/Desktop/`date +"%Y%m%d-%H%M%S"`.pcap
fi

# Touch the file so that we own it and not root (since we run tcpdump as root)
touch $OUTPUT_FILE

# Start tcpdump. We don't bother to save the following frame types, since all
# we really want to use are data (and possibly authentication) frames:
#   802.11 probe request   0x40
#   802.11 probe response  0x50
#   802.11 beacon          0x80
#   802.11 "power save"    0xA4
#   802.11 "clear to send" 0xC4
#   802.11 ACK frame       0xD4
#
# See http://www.nersc.gov/~scottc/misc/docs/snort-2.1.1-RC1/decode_8h-source.html for more.
echo "Starting packet capture..."
echo "Press control-c to quit."
echo
sudo tcpdump \
    -i $WIFICARD \
    -I \
    -n \
    -s 0 \
    -w $OUTPUT_FILE \
    not ether host $ETHER_ADDR \
    and not host $IP_ADDR \
    and not "(wlan[0:1] & 0xfc) == 0x40" \
    and not "(wlan[0:1] & 0xfc) == 0x50" \
    and not "(wlan[0:1] & 0xfc) == 0x80" \
    and not "(wlan[0:1] & 0xfc) == 0xa4" \
    and not "(wlan[0:1] & 0xfc) == 0xc4" \
    and not "(wlan[0:1] & 0xfc) == 0xd4"
