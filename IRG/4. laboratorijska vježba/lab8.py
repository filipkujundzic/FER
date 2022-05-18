import pyglet
from pyglet.gl import *
#from pyglet.window import key
#from pyglet.window import mouse
import numpy as np
import math

global width, height,eps,m,umin,umax,vmin,vmax, c
width = 500
height = 300

eps = 100
m = 16
umin = -1
umax = 1
vmin = -1.2
vmax = 1.2
c = 0.32 + 0.043j
window = pyglet.window.Window(width=width, height=height)

def divergenceTest(c_real, c_imag, m):
    #pass
    z = 0 + 0j
    for i in range(1,m+1):
        z = z ** 2 + c_real + c_imag*1j
        r = (z.real ** 2 + z.imag ** 2) ** 0.5
        if r > m**2:
            return i
    return -1

def drawmandelbrot(x, y):
    global width,height,eps,m,umin,umax,vmin,vmax

    u = ((umax - umin) * x / width) + umin
    v = ((vmax - vmin) * y / height) + vmin
    k = -1
    c = u + v * 1j
    z = 0 + 0j
    r = (z.real ** 2 + z.imag ** 2) ** 0.5
    k = divergenceTest(u, v, m)
    if k == -1:
        glColor3f(0, 0, 0);
    else:
        glColor3f(k / m, 1 - k / (2 * m), 0.8 - k / (3 * m))

    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

def drawjul(x, y):
    global width,height,eps,m,umin,umax,vmin,vmax, c

    u = (umax - umin) * x / width + umin
    v = (vmax - vmin) * y / height + vmin
    k = -1
    #r = 0
    z = u + v * 1j
    r = (z.real ** 2 + z.imag ** 2) ** 0.5
    while r < eps and k < m:
        k += 1
        z = z ** 2 + c
        r = (z.real ** 2 + z.imag ** 2) ** 0.5

        glColor3f(k / m, 1 - k / (2 * m), 0.8 - k / (3 * m))
    glColor3f(k,k,k)
    glBegin(GL_POINTS)
    glVertex2i(x, y)
    glEnd()

@window.event
def on_draw():
    global width
    global height

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    #glColor3f(0, 255, 0)
    glLoadIdentity()
    for x in range(width):
        for y in range(height):
            drawjul(x, y)
            #drawmandelbrot(x, y)

pyglet.app.run()
