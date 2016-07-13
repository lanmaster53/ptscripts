# This file was derived from dsusers.py, which is is part of ntdsxtract.
#
# ntdsxtract is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ntdsxtract is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ntdsxtract.  If not, see <http://www.gnu.org/licenses/>.

'''
@editor:        LaNMaSteR53
@author:        Csaba Barta
@license:       GNU General Public License 2.0 or later
@contact:       csaba.barta@gmail.com
'''

from ntds.dsdatabase import *
from ntds.dsrecord import *
from ntds.dslink import *
from ntds.dstime import *
from ntds.dsobjects import *

def usage():
    print "DSHashes"
    print "Extracts user hashes in a user-friendly format\n"
    print "usage: %s <datatable> <linktable> [option]" % sys.argv[0]
    print "  options:"
    print "    --rid <user rid>"
    print "          List user identified by RID"
    print "    --name <user name>"
    print "          List user identified by Name"
    print "    --passwordhashes <system hive>"
    print "          Extract password hashes"
    print "    --passwordhistory <system hive>"
    print "          Extract password history"
    print "    --exclude-disabled"
    print "          Exclude disabled accounts from output"

if len(sys.argv) < 3:
    usage()
    sys.exit(1)

rid = -1
name = ""
syshive = ""
pwdump = False
pwhdump = False
optid = 0
excl_dsbl = False
print "Running with options:"
for opt in sys.argv:
    if opt == "--rid":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        rid = int(sys.argv[optid + 1])
        print "\tUser RID: %d" % rid
    if opt == "--name":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        name = sys.argv[optid + 1]
        print "\tUser name: %s" % name
    if opt == "--passwordhashes":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        syshive = sys.argv[optid + 1]
        pwdump = True
        print "\tExtracting password hashes"
    if opt == "--passwordhistory":
        if len(sys.argv) < 5:
            usage()
            sys.exit(1)
        syshive = sys.argv[optid + 1]
        pwhdump = True
        print "\tExtracting password history"
    if '--exclude-disabled' in sys.argv:
        excl_dsbl = True
    optid += 1 

db = dsInitDatabase(sys.argv[1])
dl = dsInitLinks(sys.argv[2])

if pwdump or pwhdump:
    dsInitEncryption(syshive)

utype = -1
utype = dsGetTypeIdByTypeName(db, "Person")
if utype == -1:
    print "Unable to get type id for Person"
    sys.exit()

print "\nList of hashes:"
print "=============="
for recordid in dsMapLineIdByRecordId:
    if int(dsGetRecordType(db, recordid)) == utype:
        user = dsUser(db, recordid)
        if rid != -1 and user.SID.RID != rid:
            continue
        if name != "" and user.Name != name:
            continue
        if excl_dsbl:
            user_disabled = False
            for uac in user.getUserAccountControl():
                if uac == 'Disabled': user_disabled = True
            if user_disabled: continue

        if pwdump == True:
            nthash = ''
            lmhash = 'aad3b435b51404eeaad3b435b51404ee'
            (lm, nt) = user.getPasswordHashes()
            if nt != '':
                nthash = nt
                if lm != '':
                    lmhash = lm
            hash = "%s:%s:%s:%s:::" % (user.SAMAccountName, user.SID.RID, lmhash, nthash)
            if nt != '':
                print hash

        if pwhdump == True:
            lmhistory = None
            nthistory = None
            (lmhistory, nthistory) = user.getPasswordHistory()
            if nthistory != None:
                hashid = 0
                for nthash in nthistory:
                    print "%s_nthistory%d:%s:E52CAC67419A9A224A3B108F3FA6CB6D:%s:::" % (user.SAMAccountName, hashid, user.SID.RID, nthash)
                    hashid += 1
                if lmhistory != None:
                    hashid = 0
                    for lmhash in lmhistory:
                        print "%s_lmhistory%d:%s:%s:8846F7EAEE8FB117AD06BDD830B7586C:::" % (user.SAMAccountName, hashid, user.SID.RID, lmhash)
                        hashid += 1

if pwhdump == True:
  print "\n[*] NOTE: NT and LM hashes are shown on individual lines with the respective hash of 'password' in the opposing position."
  print "This is done in order to make sure the output plays nice with various hash cracking tools. Account for this when cracking historical hashes.\n"
