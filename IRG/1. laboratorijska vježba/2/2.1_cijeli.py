#!/usr/bin/env python3
#Bresenhamov 
from pyglet.gl import *

print()

i = input("Molim x,y koordinate početne točke? ")
pocetna = list(map(int, i.split()))

i = input("Molim x,y koordinate završne točke? ")
zavrsna = list(map(int, i.split()))

window = pyglet.window.Window()
@window.event
def on_draw():
	xs = pocetna[0]
	ys = pocetna[1]
	xe = zavrsna[0]
	ye = zavrsna[1]

	a = 2 * (ye - ys) 

	yc = ys
	yf = -(xe - xs)
	korekcija = -2*(xe-xs)
	x = xs
	for i in range(xs,xe+1):
		pyglet.graphics.draw(1,pyglet.gl.GL_POINTS,('v2i',(i,yc)))
		yf = yf + a
		if(yf >= 0):
			yf = yf + korekcija
			yc = yc + 1

	glBegin(GL_LINES)

	glVertex2i(pocetna[0],pocetna[1] + 20)
	glVertex2i(zavrsna[0],zavrsna[1] + 20)

	glEnd()

pyglet.app.run()