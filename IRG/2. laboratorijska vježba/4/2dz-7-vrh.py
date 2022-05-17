#!/usr/bin/env python3

from pyglet.gl import *
import fileinput
from itertools import *

vrhovi = []
poligoni = []
t = []
for line in fileinput.input():
	if not(line.startswith("#") or line.startswith("g") or line.startswith(" ")):
		if(line.startswith("v")):
			t = line.strip().split()
			t = list(map(float,t[1:]))
			vrhovi.append(t)
		if(line.startswith("f")):
			t = line.strip().split()
			t = list(map(int,t[1:]))
			poligoni.append(t)


i = input("Molim x,y koordinate točke? ")
tocka = list(map(float, i.split()))

window = pyglet.window.Window()
@window.event
def on_draw():
	unutar = 1
	zastavica = 0
	koefpoligona = []
	crtaj = []
	crtajtmp = []
	for p in poligoni:
		tmplista = []
		x1 = float(vrhovi[p[0]-1][0])
		y1 = float(vrhovi[p[0]-1][1])
		z1 = float(vrhovi[p[0]-1][2])
		x2 = float(vrhovi[p[1]-1][0])
		y2 = float(vrhovi[p[1]-1][1])
		z2 = float(vrhovi[p[1]-1][2])
		x3 = float(vrhovi[p[2]-1][0])
		y3 = float(vrhovi[p[2]-1][1])
		z3 = float(vrhovi[p[2]-1][2])

		crtajtmp.append(x1*8 + 300)
		crtajtmp.append(y1*8 + 300)
		crtajtmp.append(x2*8 + 300)
		crtajtmp.append(y2*8 + 300)
		crtajtmp.append(x3*8 + 300)
		crtajtmp.append(y3*8 + 300)

		a = (y2 - y1) * (z3 - z1) - (z2 - z1) * (y3 - y1)
		b = -(x2 - x1) * (z3 - z1) + (z2 - z1) * (x3 - x1)
		c = (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1)
		d = -x1 * a - y1 * b - z1 * c

		if(a * tocka[0] + b * tocka[1] + c * tocka[2] + d == 0):
			zastavica = 1
			unutar = -1
		elif(a * tocka[0] + b * tocka[1] + c * tocka[2]  + d > 0 and zastavica == 0):
			unutar = 0
		
		print(p)
		print("a ovo je:")
		print(a * tocka[0] + b * tocka[1] + c * tocka[2] + d)

		tmplista.extend((a,b,c,d))
		koefpoligona.append(tmplista)
		tmplista = []
		crtaj.append(crtajtmp)
		vlist = pyglet.graphics.vertex_list(3, ('v2f', list(crtajtmp)))
		glColor3f(0,1,0)
		vlist.draw(GL_LINE_LOOP)

		crtajtmp = []

	if(unutar == 1):
		print("Točka je unutar tijela")
	elif(unutar == 0):
		print("Točka je izvan tijela")
	elif(unutar == -1):
		print("Točka je na tijelu")




pyglet.app.run()