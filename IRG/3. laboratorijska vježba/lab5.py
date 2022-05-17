#!/usr/bin/env python3

import math
from pyglet.gl import *
import numpy
import fileinput

global ociste, glediste, vertices, faces
window = pyglet.window.Window(width = 1280, height = 720)

ociste = numpy.array([5,5,5],dtype = float)
glediste = numpy.array([0,0,0],dtype = float)


@window.event
def on_draw():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(window.width/2,window.height/2,0);
    scaling = 10#int((abs(vertices[0][0])-abs(vertices[-1][0])+.5)/4)
    glScalef(scaling,scaling,scaling);
    t = pogled(ociste,glediste)
    p = projekcija(ociste,glediste)
    renderScene(t,p)
    #renderScene()


def renderScene(t, p):
    glColor3f(1.0,0.0,0.0)
    tfp_vertices = []
    for vertex in vertices:
    	tfp_vertices.append(numpy.dot(numpy.dot(numpy.append(vertex,numpy.ones(1)),t),p))
    for face in faces:
    	glBegin(GL_LINE_LOOP)
    	glVertex2f(tfp_vertices[int(face[0])-1][0], tfp_vertices[int(face[0])-1][1])
    	glVertex2f(tfp_vertices[int(face[1])-1][0], tfp_vertices[int(face[1])-1][1])
    	glVertex2f(tfp_vertices[int(face[2])-1][0], tfp_vertices[int(face[2])-1][1])
    	glEnd()

#transformacija pogleda
def pogled(o,g):
	g = numpy.append(g,numpy.ones(1))
	#matrix t1
	t1 = numpy.identity(4)
	t1[3,0] = -o[0]
	t1[3,1] = -o[1]
	t1[3,2] = -o[2]
	#matrix t2
	g1 = numpy.dot(g,t1)
	t2 = numpy.identity(4)
	cos_alpha = g1[0]/math.sqrt(g1[0]**2 + g1[1]**2)
	sin_alpha = g1[1]/math.sqrt(g1[0]**2 + g1[1]**2)
	t2[0,0] = cos_alpha
	t2[0,1] = -sin_alpha
	t2[1,0] = sin_alpha
	t2[1,1] = cos_alpha
	#matrix t3
	g2 = numpy.dot(g1,t2)
	t3 = numpy.identity(4)
	cos_beta = g2[2]/math.sqrt(g2[0]**2 + g2[2]**2)
	sin_beta = g2[0]/math.sqrt(g2[0]**2 + g2[2]**2)
	t3[0,0] = cos_beta
	t3[0,2] = sin_beta
	t3[2,0] = -sin_beta
	t3[2,2] = cos_beta
	#matrix t4
	t4 = numpy.identity(4)
	t4[0,0] = 0
	t4[1,1] = 0
	t4[0,1] = -1
	t4[1,0] = 1
	#matrix t5
	t5 = numpy.identity(4)
	t5[0,0] = -1
	t = numpy.dot(numpy.dot(numpy.dot(numpy.dot(t1,t2),t3),t4),t5)
	return t
'''
#perspektivna projekcija
def projekcija(o,g):
	h = numpy.linalg.norm(o-g)
	xp = o[0]/o[2]*h
	yp = o[1]/o[2]*h
	p = numpy.identity(4)
	p[0][0]=xp
	p[1][1]=yp
	print(p)
	return p
'''
def projekcija(o,g):
	h = numpy.linalg.norm(o-g)
	xp = o[0]/o[2]*h
	yp = o[1]/o[2]*h
	p = numpy.identity(4)
	p[0][0] = xp
	p[1][1] = yp
	p[2][2] = 0
	p[2][3]=1/h
	p[3][3] = 0
	return p

def load_body():
	print("Upisite ime lika kojeg zelite ucitati:")
	file = input() + ".obj"
	countV = 0
	countF = 0
	with open(file,'r') as f:
		vertices = []
		faces = []
		while True:
			line = f.readline()
			if not line:
				break
			line = line.strip()
			if(len(line) == 0):
				continue
			elif line.startswith("v"):
				splitted = line.split(" ",1)
				vertices.append(numpy.fromstring(splitted[1],dtype = float, sep = " "))
			elif line.startswith("f"):
				splitted = line.split(" ",1)
				faces.append(numpy.fromstring(splitted[1],dtype = float, sep = " "))
	print("Tijelo uspjesno ucitano")
	return numpy.array(vertices), numpy.array(faces)

if __name__ == "__main__":
    global vertices, faces
    vertices,faces = load_body()
    pyglet.app.run()

