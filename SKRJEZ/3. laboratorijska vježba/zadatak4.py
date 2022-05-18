#!/usr/bin/python

import sys
import urllib.request
import re

adresa = sys.argv[1]
stranica = urllib.request.urlopen(adresa)
mybytes = stranica.read()
mystr = mybytes.decode("utf8")
'''
print("Ispis stranice:")
print("-"*80)
print(mystr)
print("-"*80)
'''

print("\nLinkovi:")
linkovi = re.findall(r'href=[\'"]?(http[s]{0,1}[^\'" >]+)', mystr) 

for link in linkovi:
	print(link)

print("\n\nHostovi:")
hostref = {}
for link in linkovi:
	host = link.split("/")
	h = host[2]
	if(host[2].startswith("www.")):
		h = str(host[2])
		h = h[4:]
	if(host[2].endswith("/")):
		h = str(host[2])
		h = h[:-1]

	if(hostref.get(h,0) == 0):
		hostref[h] = 1
	else:
		hostref[h] += 1

for (k,v) in hostref.items():
    print("{0:25s} : {1:3d}".format(k,v))

print("\n\ne-mail adrese:")
email = re.findall("([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})", mystr)
for mail in email:
	print(mail)

print("\n\nLinkovi na slike:")
pictures = re.findall('<img[\s]+src="[^"]+"[^>]+>', mystr)    
for pic in pictures:
	print(pic)