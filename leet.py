#!/usr/bin/python -tt

import sys

leetdict = { \
'a':['4','@'], \
'e':['3'], \
'g':['6'], \
'i':['1','!'], \
'l':['7','1','!'], \
'n':['^'], \
'o':['0'], \
'q':['0'], \
's':['5','$'], \
't':['7'], \
'v':['\/'], \
}

# for JTR
# X = position
# Y = letter
# Z = leet substitiute
#rule = '=XYoXZ'
def jtr(num):
  print '[List.Rules:Wordlist]'
  for key in leetdict.keys():
    for val in leetdict[key]:
      for i in range(int(num)):
        print '=%s%so%s%s' % (i, key, i, val)
  
def usage():
  print """
leet.py - Tim Tomes (@LaNMaSteR53) (www.lanmaster53.com)

Usage:
  ./leet.py [options]
Options:
  -h          - This screen
  -c          - Swap case of all letters
  -f <file|-> - Wordlist to mangle. '-' is stdin
  -v          - View leet speak dictionary
  -b <#chars> - Build a John The Ripper leet mangle rule for words <#chars> long.
                - Uses custom mangle dictionary as seen with '-v'
                - Not as thorough.
  """

def case(wordlist):
  for word in wordlist:
    for i in range(len(word)):
      chars = list(word)
      chars[i] = chars[i].swapcase()
      neword = ''.join(chars)
      if not neword in wordlist:
        wordlist.append(neword)
  return wordlist

def leet(wordlist):
  for word in wordlist:
    for i in range(len(word)):
      chars = list(word)
      if chars[i].lower() in leetdict.keys():
        for x in leetdict[chars[i].lower()]:
          chars[i] = x
          neword = ''.join(chars)
          if not neword in wordlist:
            wordlist.append(neword)
  return wordlist

wordlist = []

if len(sys.argv) == 3 and sys.argv[1] == '-b':
  jtr(sys.argv[2])
  sys.exit()
if len(sys.argv) == 2 and sys.argv[1] == '-v':
  for key in sorted(leetdict.keys()):
    print '%s:%s' % (key,','.join(leetdict[key]))
  sys.exit()
if '-h' in sys.argv:
  usage()
  sys.exit()
if '-f' in sys.argv and len(sys.argv) >= 3:
  filename = sys.argv[sys.argv.index('-f') + 1]
  if filename == '-':
    wordlist = sys.stdin.read().split()
  else:
    wordlist = open(filename).read().split()
if '-c' in sys.argv:
  wordlist = case(wordlist)
if wordlist == []:
  usage()
  sys.exit()

wordlist = leet(wordlist)
for word in sorted(wordlist):
  print word
