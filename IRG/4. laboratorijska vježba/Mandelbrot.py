import pyglet
from pyglet.gl import *
#from pyglet.window import key
#from pyglet.window import mouse
import numpy as np
import math

global width, height,eps,m,umin,umax,vmin,vmax,c,xmin,xmax,ymin,ymax,epsilon,limit
epsilon = 100

width = 1280
height = 720
xmin = 0  
xmax = 599 
ymin = 0 
ymax = 599 
umin = 2 * (-1)
umax = 1 
vmin = 1.2 * (-1)
vmax = 1.2 
limit = 16

window = pyglet.window.Window(width=width, height=height)

def divergence_test(c_re, c_im, limit):
	global epsilon
	z_re = 0
	z_im = 0

	for i in range(1, limit + 1):
		next_re = z_re * z_re - z_im * z_im + c_re
		next_im = 2 * z_re * z_im + c_im
		z_re = next_re
		z_im = next_im
		modul2 = z_re * z_re + z_im * z_im
		if(modul2 > epsilon*epsilon):
			return i

	return -1


def renderScene():
	limit = 16
	glPointSize(1)
	glBegin(GL_POINTS)
	for y in range(ymin,ymax + 1):
		for x in range(xmin, xmax + 1):
			c_re = (x - xmin) / (xmax - xmin) * (umax - umin) + umin 
			c_im = (y - ymin) / (ymax - ymin) * (vmax - vmin) + vmin
			n = divergence_test(c_re, c_im, 16) 
			if(n == -1):
				glColor3f(0.0,0.0,0.0)
			else:
				glColor3f(n/limit,1-(n/(2.0 * limit)),0.8-(n/(3.0 * limit)))
			glVertex2i(x,y)
	glEnd()


@window.event
def on_draw():
    global width
    global height

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(0, 255, 0)
    glLoadIdentity()
    renderScene()

pyglet.app.run()