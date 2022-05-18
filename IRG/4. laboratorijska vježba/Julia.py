import pyglet
from pyglet.gl import *
#from pyglet.window import key
#from pyglet.window import mouse
import numpy as np
import math

global width, height,eps,m,umin,umax,vmin,vmax,c,xmin,xmax,ymin,ymax
width = 1280
height = 720
xmin = 0  
xmax = 599 
ymin = 0 
ymax = 599 
umin = 1 * (-1)
umax = 1 
vmin = 1.2 * (-1)
vmax = 1.2 

window = pyglet.window.Window(width=width, height=height)

def divergence_test(z0_re, z0_im, c_re, c_im, limit, epsilonSquare):
	z_re = z0_re
	z_im = z0_im

	modul2 = z_re * z_re + z_im * z_im
	if(modul2 > epsilonSquare):
		return 0

	for i in range(1, limit + 1):
		next_re = z_re * z_re - z_im * z_im + c_re
		next_im = 2 * z_re * z_im + c_im
		z_re = next_re
		z_im = next_im
		modul2 = z_re * z_re + z_im * z_im
		if(modul2 > epsilonSquare):
			return i

	return -1

def maks(a, b):
	if(b > a):
		return b
	else:
		return a

def renderScene():
	limit = 64
	c_re = 0.32 
	c_im = 0.043 

	epsilon =  maks(c_re * c_re + c_im * c_im, 2.0)
	epsilonSquare = epsilon * epsilon
	glPointSize(1)
	glBegin(GL_POINTS)
	for y in range(ymin,ymax + 1):
		for x in range(xmin, xmax + 1):
			z0_re = (x - xmin) / (xmax - xmin) * (umax - umin) + umin 
			z0_im = (y - ymin) / (ymax - ymin) * (vmax - vmin) + vmin
			n = divergence_test(z0_re, z0_im, c_re, c_im, limit, epsilonSquare) 
			if(n == -1):
				glColor3f(0.0,0.0,0.0)
			else:
				glColor3f(n/limit,1-(n/limit/2.0),0.8-(n/limit/3.0))
			glVertex2i(x,y)
	glEnd()


@window.event
def on_draw():
    global width
    global height

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    #glColor3f(0, 255, 0)
    glLoadIdentity()
    renderScene()

pyglet.app.run()