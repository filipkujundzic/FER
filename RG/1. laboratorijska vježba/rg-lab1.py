import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from math import factorial
import math
smjer=1
brojac=0.1
tocke=[]

tocke=[]
tocke.append([0,0,0,1])
tocke.append([0, 10, 5, 1])
tocke.append([10, 10, 10, 1])
tocke.append([10, 0, 15 ,1])
tocke.append([0, 0, 20 ,1])
tocke.append([0, 10, 25 ,1])
tocke.append([10, 10, 30 ,1])
tocke.append([10, 0, 35 ,1])
tocke.append([0, 0, 40 ,1])
tocke.append([0, 10, 45 ,1])
tocke.append([10, 10, 50 ,1])
tocke.append([10, 0, 55 ,1])
tocke = np.array(tocke)
n=len(tocke)


#čitanje iz datoteke
with open("ptica.obj", "r") as f:
    txt=f.readlines()
v=[]
f=[]
for line in txt:
    if(line[0] == 'v'):
        v.append(line[1:].split())
    elif(line[0] == 'f'):
        f.append(line[1:].split())

for i in range(len(f)):
    for j in range(3):
        f[i][j] = int(f[i][j])
        f[i][j]-=1
for i in range(len(v)):
    for j in range(3):
        v[i][j] = float(v[i][j])
v=np.array(v)

def norm_vector(vector):
    suma=0
    for i in range(len(vector)):
        suma+=vector[i]
    dj=np.sqrt(suma)
    return np.array([vector[0]/dj, vector[1]/dj, vector[2]/dj])

def mat_rot(os, alfa):
    os=norm_vector(os)
    sigma1 = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [-os[0], -os[1], -os[2], 1]])
    sigma2 = np.array([[math.cos(alfa), math.sin(alfa), 0, 0], [-math.sin(alfa), math.cos(alfa), 0, 0],[0,0,1,0],[0,0,0,1]])
    sigma3 = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,0], [os[0], os[1], os[2], 1]])
    
    return np.dot(np.dot(sigma1,sigma2), sigma3)
    
def mat_trans(pt):
    return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0],[pt[0], pt[1], pt[2], 1]])

def dotproduct(v1, v2):
  return sum((a*b) for a, b in zip(v1, v2))

def length(v):
  return math.sqrt(dotproduct(v, v))

def angle(v1, v2):
  return math.acos(round(dotproduct(v1, v2) / (length(v1) * length(v2)),3))

def convertToDeg(kut):
    return kut *180/math.pi

def racunaj_os_i_kut(poc, cilj, t):
    os = np.cross(poc[:3], cilj[t][:3])
    kut = angle(poc, cilj[round(t,2)])
    kutUStupnjevima = convertToDeg(kut)
    return os, kutUStupnjevima

def vrati_4_tocke(index):
    return np.array([tocke[index], tocke[index+1], tocke[index+2], tocke[index+3]])


matrica2 = np.array([[-1/6,3/6,-3/6,1/6],[3/6,-1,3/6,0],[-3/6,0,3/6,0],[1/6,4/6,1/6,0]])
matrica  = np.array([[-0.5,1.5,-1.5,0.5],[1,-2,1,0],[-0.5,0,0.5,0]])


poc = np.array([0,0,1, 1]) #pocetna orijentacija - proizvoljno zadana

def izrCilj():
    global odabrane_tocke
    global poc
    global tocke
    lista_ciljeva=[]

    odabrane_tocke=0
    for i in range(len(tocke)-3):
        cilj=dict()
        cilj = {round(new_list,2): [] for new_list in np.arange(0,1,0.01)}
        chosen_tocke=None
        chosen_tocke = vrati_4_tocke(odabrane_tocke)
        
        for t in np.arange(0, 1, 0.01):
            t=round(t,2)
            uk = np.dot((3/8)*np.array([t*t*t, t*t, t, 1]), np.dot(matrica2, chosen_tocke))
            cilj[t] = uk
        lista_ciljeva.append(cilj)
        odabrane_tocke+=1
    return lista_ciljeva

def izrOrj():
    global odabrane_tocke
    global poc
    global tocke
    lista_orj=[]
    odabrane_tocke=0
    for i in range(len(tocke)-3):
        orj =dict()
        orj = {round(new_list,2): [] for new_list in np.arange(0,1,0.01)}
        chosen_tocke=None
        chosen_tocke = vrati_4_tocke(odabrane_tocke)
        
        for t in np.arange(0, 1, 0.01):
            t=round(t,2)
            uk=np.dot(np.array([t*t, t, 1]), np.dot(matrica,chosen_tocke))
            orj[t] = uk
        lista_orj.append(orj)
        odabrane_tocke+=1
    return lista_orj

lista_ciljeva = izrCilj() # formula 1.2
lista_ciljna_orijentacija = izrOrj() # formula 1.4
koja_tocka=0
def funkcija():
    global v, f
    global brojac
    global cilj
    global poc
    global lista_ciljna_orijentacija
    global koja_tocka

    crtanje = []

    os, alfa = racunaj_os_i_kut(poc, lista_ciljna_orijentacija[koja_tocka], brojac)

    potrebna_translacija = lista_ciljeva[koja_tocka][brojac]

    matrica_rotacije = mat_rot(os, alfa)

    matrica_translac = mat_trans(potrebna_translacija)

    for i,tocka in enumerate(v):
        tockaV = np.insert(tocka, len(tocka), 1)
        crtanje.append(tockaV)
    

    x1l=[]
    y1l=[]
    x2l=[]
    y2l=[]
    x3l=[]
    y3l=[]
    z1l=[]
    z2l=[]
    z3l=[]

    for i,poligon in enumerate(f):
        for j,svaki in enumerate(poligon):
            if j==0:
                x1=crtanje[svaki][0]
                y1=crtanje[svaki][1]
                z1=crtanje[svaki][2]
                x1l.append(x1)
                y1l.append(y1)
                z1l.append(z1)
            elif j==1:
                x2=crtanje[svaki][0]
                y2=crtanje[svaki][1]
                z2=crtanje[svaki][2]
                x2l.append(x2)
                y2l.append(y2)
                z2l.append(z2)
            elif j==2:
                x3=crtanje[svaki][0]
                y3=crtanje[svaki][1]
                z3=crtanje[svaki][2]
                x3l.append(x3)
                y3l.append(y3)
                z3l.append(z3)
    
    return x1l,y1l,x2l,y2l,x3l,y3l,z1l,z2l,z3l,os,alfa,potrebna_translacija,lista_ciljeva,lista_ciljna_orijentacija


def nacrtajObjekt(x1l,y1l,x2l,y2l,x3l,y3l,z1l,z2l,z3l):
    for i in range(len(x1l)):
        glBegin(GL_LINE_LOOP)
        glVertex3f(x1l[i],y1l[i],z1l[i])
        glVertex3f(x2l[i],y2l[i],z2l[i])
        glVertex3f(x3l[i],y3l[i],z3l[i])
        glEnd()

def nacrtajKrivulju(cilj):
    glColor3f(1, 1.0, 1.0)
    
    for segment in range(len(cilj)):
        glBegin(GL_LINE_STRIP)
        for i in np.arange(0, 1, 0.01):
            i=round(i,2)
            glVertex3f(cilj[segment][i][0], cilj[segment][i][1], cilj[segment][i][2])
        glEnd()

def nacrtajTangentu(cilj, brojac, orijentir):
    global koja_tocka

    glColor3f(1.0,0.0,128/255)
    glLineWidth(5)
    
    glBegin(GL_LINES)
    glVertex3f(cilj[koja_tocka][brojac][0], cilj[koja_tocka][brojac][1], cilj[koja_tocka][brojac][2])
    
    glVertex3f((1/6)*orijentir[koja_tocka][brojac][0], (1/6)*orijentir[koja_tocka][brojac][1], (1/6)*orijentir[koja_tocka][brojac][2])

    glEnd()
    
def nacrtajTocke():
    global tocke
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.0, 1.0)
    glVertex3f(0,0,0)
    glEnd()
    
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.0, 1.0)
    glVertex3f(0,10,5)
    glEnd()
    
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.0, 1.0)
    glVertex3f(10,10,10)
    glEnd()
    
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.0, 1.0)
    glVertex3f(10,0,15)
    glEnd()
    
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.5, 1.0)
    glVertex3f(10,0,0)
    glEnd()
    
    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.5, 1.0)
    glVertex3f(0,10,0)
    glEnd()

    glPointSize(16)
    glBegin(GL_POINTS)
    glColor3f(0.5, 0.5, 1.0)
    glVertex3f(0,0,10)
    glEnd()
    
def crtajOsi():
    
    glColor3f(1.0,0.0,0.0) #red x
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex3f(-4.0, 0.0, 0.0)
    glVertex3f(16.0, 0.0, 0.0)
    glEnd()

    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex3f(16.0, 0.0, 0.0)
    glVertex3f(15.0, 1.0, 0.0)

    glVertex3f(16.0, 0.0, 0.0)
    glVertex3f(15.0, -1.0, 0.0)
    glEnd()
    glFlush()
    
    
    glLineWidth(1)
    glColor3f(0.0,1.0,0.0) #green y
    glBegin(GL_LINES)
    glVertex3f(0.0, -4.0, 0.0)
    glVertex3f(0.0, 16.0, 0.0)
    glEnd()

    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex3f(0.0, 16.0, 0.0)
    glVertex3f(1.0, 15.0, 0.0)
    
    glVertex3f(0.0, 16.0, 0.0)
    glVertex3f(-1.0, 15.0, 0.0)
    glEnd()
    glFlush()

    
    
    glColor3f(0.0,0.0,1.0) # blue z
    glLineWidth(1)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0 , -4.0 )
    glVertex3f(0.0, 0.0 , 16.0)
    glEnd()
    
    glLineWidth(2)
    glBegin(GL_LINES)
    glVertex3f(0.0, 0.0 ,16.0)
    glVertex3f(0.0, 1.0 ,15.0)
 
    glVertex3f(0.0, 0.0, 16.0)
    glVertex3f(0.0, -1.0, 15.0)
    glEnd()
    #glFlush()

def renderScene():
    
    x1l,y1l,x2l,y2l,x3l,y3l,z1l,z2l,z3l,os,alfa,pot_tra,lista_ciljeva,lista_ciljna_orijentacija = funkcija()

    glPushMatrix()
    glTranslate(pot_tra[0],pot_tra[1],pot_tra[2])
    glRotate(alfa,os[0],os[1],os[2])
    glScale(.55,.55,.55)
    nacrtajObjekt(x1l,y1l,x2l,y2l,x3l,y3l,z1l,z2l,z3l)
    glPopMatrix()

    nacrtajKrivulju(lista_ciljeva)
    
    nacrtajTangentu(lista_ciljeva, brojac,lista_ciljna_orijentacija)
    
    nacrtajTocke()
    
    crtajOsi()
    
    mijenjaj_ociste_glediste_bezier()


def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1.0, 1.0, 1.0)
    glLoadIdentity()
    glPushMatrix()
    glTranslatef(-3, -1, -13.0); 
    glRotate(10, 1, 0, 0)
    glRotate(30, 0, 1, 0)  
    glScalef(0.55,0.55,0.55)
    renderScene()
    
    glPopMatrix()
    glutSwapBuffers()

def reshape(width,height):
    glViewport(0, 0, GLsizei(width) , GLsizei(height))
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    glMatrixMode(GL_MODELVIEW)


def mijenjaj_ociste_glediste_bezier():
    global O,G,p,smjer,brojac,koja_tocka

    if(brojac ==  0.99):
        koja_tocka+=1
        brojac = 0.00
    elif(brojac == 0.99 and koja_tocka==len(tocke)-3):
        smjer = (-1)*smjer
    else:
        brojac+=0.01
        brojac=round(brojac,2)

#INIT
glutInit()
glutInitDisplayMode(GLUT_DOUBLE) # dva graficka spremnika- prikaz na zaslonu a u drugi se crta slijedeca scena
glutInitWindowSize(1900,900)
glutInitWindowPosition(5,5)
glutCreateWindow("1. domaca zadaca u Pythonu iz RG")
glutDisplayFunc(display)
glutReshapeFunc(reshape)

glutIdleFunc(display)
glutMainLoop()