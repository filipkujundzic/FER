#!/usr/bin/env python3

import math
from pyglet.gl import *
import numpy as np
import fileinput
from pyglet.window import key
from pyglet.window import mouse

global ociste, glediste, vertices, faces, r, points, time, ind, show_curve
time = 0
show_curve = True
window = pyglet.window.Window(width=1280, height=720)

ociste = np.array([5,4,3],dtype=float)
glediste = np.array([0,0,0],dtype=float)
ind = 0

points = []

@window.event
def on_mouse_press(x,y,button, modifiers):
    global vertices, faces, ociste, points, ind, show_curve
    if button & key.LEFT:
        ociste = points[ind]
        ind += 1
        show_curve = False
    on_draw()

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(gl.GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(gl.GL_MODELVIEW)

@window.event
def on_draw():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(window.width/2,window.height/2,0);
    scaling = 100#int((abs(vertices[0][0])-abs(vertices[-1][0])+.5)/4)
    glScalef(scaling,scaling,scaling);
    t=myLookAt(ociste,glediste)
    p=myFrustum(ociste,glediste)
    renderScene(t,p)
    #renderScene()

def renderScene(t,p):
    if show_curve: draw_curve()
    glColor3f(1.0,0.0,0.0)
    tfp_vertices = []
    for vertex in vertices:
        tfp_vertices.append(np.dot(np.dot(np.append(vertex,np.ones(1)),t),p))
        tfp_vertices[-1] /= tfp_vertices[-1][3]
    for face in faces:
        prvi = np.array([tfp_vertices[int(face[0])-1][0], tfp_vertices[int(face[0])-1][1],0])
        drugi = np.array([tfp_vertices[int(face[1])-1][0], tfp_vertices[int(face[1])-1][1],0])
        treci = np.array([tfp_vertices[int(face[2])-1][0], tfp_vertices[int(face[2])-1][1],0])
        if direction(prvi,drugi,treci): continue
        glBegin(GL_LINE_LOOP)
        glVertex2f(tfp_vertices[int(face[0])-1][0], tfp_vertices[int(face[0])-1][1])
        glVertex2f(tfp_vertices[int(face[1])-1][0], tfp_vertices[int(face[1])-1][1])
        glVertex2f(tfp_vertices[int(face[2])-1][0], tfp_vertices[int(face[2])-1][1])
        glEnd()


def direction(v1,v2,v3):
    e1=(v2[0]-v1[0])*(v2[1]+v1[1])
    e2=(v3[0]-v2[0])*(v3[1]+v2[1])
    e3=(v1[0]-v3[0])*(v1[1]+v3[1])
    if (e1+e2+e3 > 0):
        return True
    else:
        return False

def bernstein_polyonimal(n, i, t):    
    return math.factorial(n)/(math.factorial(i)*math.factorial(n-i)) * math.pow(t,i) * math.pow(1-t,n-i)

def draw_curve():
    global points
    glColor3f(0.0,1.0,0.0)
    for p in points:
        glBegin(GL_POINTS)
        glVertex2f(p[0],p[1])
        glEnd()

def calc_points():
    global r
    n = len(r)
    ts = np.linspace(0,1,101)
    global points
    for t in ts:
        p = np.zeros(3)
        for i in range(n):
            p += r[i].dot(bernstein_polyonimal(n,i,t))
        points.append(p)

def load_ctrl_points():
    global r
    file = "kontrolne_tocke.txt"
    ctrl_ps = []
    with open(file,'r') as f:
        while True:
            line = f.readline()
            if not line:
                break
            line = line.strip()
            if(len(line) == 0):
                continue
            else:
                ctrl_ps.append(np.fromstring(line,dtype=float,sep=" "))
    r = ctrl_ps
    calc_points()

def update(update):
    global time
    time=update+time

def myLookAt(o,g):
    g = np.append(g,np.ones(1))
    #matrix t1
    t1 = np.identity(4)
    t1[3,0] = -o[0]
    t1[3,1] = -o[1]
    t1[3,2] = -o[2]
    #matrix t2
    g1 = np.dot(g,t1)
    t2 = np.identity(4)
    cos_alpha = g1[0]/math.sqrt(g1[0]**2 + g1[1]**2)
    sin_alpha = g1[1]/math.sqrt(g1[0]**2 + g1[1]**2)
    t2[0,0] = cos_alpha
    t2[0,1] = -sin_alpha
    t2[1,0] = sin_alpha
    t2[1,1] = cos_alpha
    #matrix t3
    g2 = np.dot(g1,t2) 
    t3 = np.identity(4)
    cos_beta = g2[2]/math.sqrt(g2[0]**2 + g2[2]**2)
    sin_beta = g2[0]/math.sqrt(g2[0]**2 + g2[2]**2)
    t3[0,0] = cos_beta
    t3[0,2] = sin_beta
    t3[2,0] = -sin_beta
    t3[2,2] = cos_beta
    #g3 = np.dot(g2,t3)
    #matrix t4
    t4 = np.identity(4)
    t4[0,0] = 0
    t4[1,1] = 0
    t4[0,1] = -1
    t4[1,0] = 1
    #matrix t5
    t5 = np.identity(4)
    t5[0,0] = -1
    t = np.dot(np.dot(np.dot(np.dot(t1,t2),t3),t4),t5)
    return t

def myFrustum(o,g):
    #a = np.append(a,np.ones(1))
    h = np.linalg.norm(o-g)
    xp = o[0]/o[2]*h
    yp = o[1]/o[2]*h
    p = np.identity(4)
    #p[0][0]=xp
    #p[1][1]=yp
    p[2,2]=0
    p[2,3]=1/h
    p[3][3] = 0
    return p

def load_body():
	print("upisite ime lika kojeg zelite ucitati:")
	file = input() + ".obj"
	countV = 0
	countF = 0
	with open(file,'r') as f:
		vertices = []
		faces  = []
		while True:
			line = f.readline()
			if not line:
				break
			line = line.strip()
			if(len(line) == 0):
				continue
			elif line.startswith("v"):
				splitted = line.split(" ",1)
				vertices.append(np.fromstring(splitted[1],dtype=float,sep=" "))
			elif line.startswith("f"):
				splitted = line.split(" ",1)
				faces.append(np.fromstring(splitted[1],dtype=float,sep=" "))
	print("Tijelo uspjesno ucitano")
	return np.array(vertices), np.array(faces)

if __name__ == "__main__":
    global vertices, faces
    load_ctrl_points()
    vertices,faces = load_body()
    pyglet.clock.schedule_interval(update, 0.1)
    pyglet.app.run()
