#!/usr/bin/env python

import sys, curses
from scapy.all import *

# interface should be first variable givven on the command line
if len(sys.argv) < 2:
  print 'Must define a sniffing interface.\nExiting...'
  sys.exit()
else:
  interface = sys.argv[1]

clients = {}
pcount = 0
mgmtcount = 0

def sniffmgmt(p):
  global pcount, mgmtcount
  pcount += 1
  if p.haslayer(Dot11):
    if p.type == 0 and p.subtype ==4 and p.getfieldval('info') != '':
      mgmtcount += 1
      if p.addr2 not in clients.keys():
        clients[p.addr2] = [p.getfieldval('info')]
      else:
        if not p.getfieldval('info') in clients[p.addr2]:
          clients[p.addr2].append(p.getfieldval('info'))
  output()

def output():
  output = ''
  output += 'Total Packets:  %s\nProbe Requests: %s\n' % (str(pcount), str(mgmtcount))
  output += '=========================\n'
  for key in clients.keys():
    output += '%s - %s\n' % (key, clients[key])
  window.addstr(1, 0, output)
  window.refresh()
  
try:
  window = curses.initscr()
  sniff(iface=interface, prn=sniffmgmt, store=0)
  curses.echo()
  curses.nocbreak()
  curses.endwin()
  print 'Exiting...'
except:
  curses.echo()
  curses.nocbreak()
  curses.endwin()
  traceback.print_exc()
  print 'Exiting...'

#packets = rdpcap('traffic.pcap')
#for packet in packets:
#  sniffmgmt(packet)
