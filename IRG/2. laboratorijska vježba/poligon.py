#!/usr/bin/env python3
#ucitavanje vrhova poligona s tipkovnice
from pyglet.gl import *
from itertools import *
import fileinput

svivrhovi = []
i = 0
for line in fileinput.input():
	if(i == 0):
		a = line.strip().split()
	else:
		svivrhovi.append(list(map(int, line.split())))
	i = i + 1

brojvrhova = int(a[0])
point = svivrhovi[-1]
del svivrhovi[-1]


#brojvrhova = input("Molim broj vrhova poligona? ")
#brojvrhova = int(fin.readline().strip())
#print(brojvrhova)

#svivrhovi = []
#p = 0
#for line in fin.readlines():
#	svivrhovi.append(list(map(int, line.split())))
#	if(line.startswith(" ")):
#		break


#print(svivrhovi)
#for i in range(0,int(brojvrhova)):
#	vrh = input("Molim koordinate vrha? ")
#	svivrhovi.append(list(map(int, vrh.split())))

#i = input("Molim koordinate točke? ")
#point = list(map(int, i.split()))

vx = point[0] 
vy = point[1]

listax = []
listay = []

window = pyglet.window.Window()
@window.event
def on_draw():

	glBegin(GL_LINES)

	for x in svivrhovi:
		listax.append(x[0])
		listay.append(x[1])
		
	xmin = min(listax)
	xmax = max(listax)
	ymin = min(listay)
	ymax = max(listay)

	licycle = cycle(svivrhovi)
	nextelem = next(licycle)
	for x in svivrhovi:
		thiselem, nextelem = nextelem, next(licycle)
		glVertex2i(thiselem[0],thiselem[1])
		glVertex2i(nextelem[0],nextelem[1])

	glEnd()
	licycle = cycle(svivrhovi)
	nextelem = next(licycle)

	ai = [] 
	bi = []
	ci = []
	unutar = 1
	iterator = 0
	nabridu = 0
	for x in svivrhovi:
		thiselem, nextelem = nextelem, next(licycle)
		ai.append(thiselem[1] - nextelem[1])
		bi.append(-thiselem[0] + nextelem[0])
		ci.append(thiselem[0] * nextelem[1] - nextelem[0] * thiselem[1])
		if(vx*ai[iterator] + vy*bi[iterator] + ci[iterator] > 0 and nabridu == 0):
			unutar = 0
		if(vx*ai[iterator] + vy*bi[iterator] + ci[iterator] == 0):
			nabridu = 1
		iterator = iterator + 1

	if(unutar == 1 and nabridu == 0):
		print("Točka je unutar poligona")
	elif(unutar == 0 and nabridu == 0):
		print("Točka nije unutar poligona")
	
	if(nabridu == 1):
		print("Točka je na bridu poligona")


	glBegin(GL_LINES)

	#bojanje poligona
	for y0 in range(ymin,ymax + 1):
		L = xmin
		D = xmax

		for a in range(0,int(brojvrhova)):
			if(ai[a] != 0):
				x1 = (-bi[a]*y0 - ci[a]) / ai[a]
				if(a == int(brojvrhova) - 1):
					if(listay[a] < listay[0]):
						if(x1 > L):
							L = x1
					if(listay[a] >= listay[0]):
						if(x1 < D):
							D = x1
				else:
					if(listay[a] < listay[a+1]):
						if(x1 > L):
							L = x1
					if(listay[a] >= listay[a+1]):
						if(x1 < D):
							D = x1

		if(L < D):
			glVertex2i(int(L),y0)
			glVertex2i(int(D),y0)

	glEnd()

pyglet.app.run()

