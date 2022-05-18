#!/usr/bin/python

q = list(range(10,100,10))
j = 0

s="Hyp"
for i in q:
	s+='#Q'+str(i)
print(s)

with open("ulazHD.txt") as f:
	for line in f:
		if(line != '\n'):
			tmp = list(line.strip().split())
			tmp = list(map(float,tmp))
			tmp.sort()
			j += 1
			p = "{0:03}".format(j)
			for i in q:
				index = int(len(tmp)*i/100)
				p += "#" + str(tmp[index]) 
			print(p)
		elif(line =='\n'):
			print("Da")

