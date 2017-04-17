#!/usr/bin/python
import sys,string

"""
-mak
This simply takes the ldif generated by newyear_ldif.py
and builds it into an ldapmodify formatted ldif.

To be used with the ldap modify query below
ldapmodify -x -D cn=root,ou=ldap,o=redbrick -y /etc/ldap.secret -f [LDIF_FROM_THIS_SCRIPT]
"""

yearsPaid = ''
uid = ''

#print modify ldif template
def modifyTemplate(uid,yearsPaid,newbie,reserved):
	if uid != '' and yearsPaid != '' and reserved == False:
		modTemp = "dn: uid="+uid.strip()+"\nchangetype: modify\nreplace: yearsPaid\nyearsPaid: "+yearsPaid.strip()+"\n"
		if newbie == '1':
			modTemp += "-\nreplace: newbie\nnewbie: FALSE\n\n"
		else:
			modTemp += "\n"
		print modTemp

#open ldif
with open(sys.argv[1], 'r') as content:
    ldif = content.read()
#split by user
getdn = string.split(ldif, 'dn: uid=')
for i in range(1,len(getdn)):
	thisdn = getdn[i].split('\n')
	newbie = 'NONE'
	reserved = False
	#split by users variables
	for j in range(0,len(thisdn)):
		x = thisdn[j].rstrip()
		uid = thisdn[0].rstrip()
		if 'reserved' in uid:
			reserved = True
		try: 
			if x.startswith("yearsPaid:"):
				yearsPaid = str(int(x.split()[1])).strip()
			elif x.startswith("newbie:"):
				newbie = '1'
			else:	continue
		except IndexError:
			break
	modifyTemplate(uid,yearsPaid,newbie,reserved)
