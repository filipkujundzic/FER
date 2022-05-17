import math
import numpy as np
from pyglet.gl import *
from pyglet.window import key
from pyglet.window import mouse

global ociste, glediste, vertices, faces, izvor, zadatak
global brojac 
window = pyglet.window.Window(width=1280, height=720)

ociste = np.array([8,0,5],dtype=float)
glediste = np.array([0,0,0],dtype=float)


#izvor = None
izvor = np.array([5,0,3],dtype = float)

zadatak = 3
#zicna forma tijela
#zadatak = 0
#konstantno sjencanje
#zadatak = 2
#Gouraudovo sjencanje 
#zadatak = 3


@window.event
def on_mouse_press(x, y, button, modifiers):
    global vertices, faces
    if button and mouse.LEFT:
        load_body()
        on_draw()

@window.event
def on_resize(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1, 1)
    glMatrixMode(GL_MODELVIEW)

@window.event
def on_draw():
    zovi = 0
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #glViewport(0, 0, window.width, window.height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, window.width/window.height, 0.5, 30.0) 
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(ociste[0], ociste[1], ociste[2], glediste[0], glediste[1], glediste[2], 0.0, 1.0, 0.0)

    if izvor.any() != None and zadatak == 2:
        zovi = 1
    if izvor.any() != None and zadatak == 3:
        zovi = 2

    xmax, ymax, zmax = max(vertices[:,0]), max(vertices[:,1]), max(vertices[:,2])
    xmin, ymin, zmin = min(vertices[:,0]), min(vertices[:,1]), min(vertices[:,2])

    velicina_x, velicina_y, velicina_z = xmax - xmin, ymax - ymin, zmax - zmin
    srediste_x, srediste_y, srediste_z = (xmax + xmin)/2, (ymax + xmin)/2, (zmax + zmin)/2
    
    scaling = 2/max(velicina_x, velicina_y, velicina_z)
    glTranslatef(-srediste_x, -srediste_y, -srediste_z)
    glScalef(scaling,scaling,scaling)
    renderScene()
    if(zovi == 1):
        konstantno()
    if(zovi == 2):
        Gouraud()

global normalarray 
global pointarray 
global tmp
global G_normalarray
global G_pointarray

def renderScene():
    global normalarray,tmp,pointarray,G_normalarray, G_pointarray
    normalarray = []
    tmp = []
    pointarray = []
    G_normalarray = []
    G_pointarray = []
    brojac = 0
    glColor3f(1.0, 1.0,0.0)
    for face in faces:
        point1 = vertices[int(face[0])-1]
        point2 = vertices[int(face[1])-1]
        point3 = vertices[int(face[2])-1]
        tmp.append(point1)
        tmp.append(point2)
        tmp.append(point3)

        # određivanje i uklanjanje stražnjih poligona
        normal = np.cross(point2-point1,point3-point1)

        if(np.dot(ociste,normal) > 0):
            pointarray.append(np.array(tmp))
            normalarray.append(np.array(normal))

        G_pointarray.append(np.array(tmp))     # za Gouraudovo sjencanje
        G_normalarray.append(np.array(normal))    # za Gouraudovo sjencanje

        tmp[:] = []
        if(zadatak == 0):
            glBegin(GL_LINE_LOOP)
            glVertex2f(point1[0], point1[1])
            glVertex2f(point2[0], point2[1])
            glVertex2f(point3[0], point3[1])
            glEnd()


def load_body():
    global vertices, faces
    #print("upisite ime lika kojeg zelite ucitati:")
    #file = input() + ".obj"
    file = "kocka.obj"
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
    vertices, faces = np.array(vertices), np.array(faces)

def konstantno():
    Ia = 256
    ka = 0.3
    Ii = 256
    kd = 0.78125

    for i in range(0,len(pointarray)):
        
        maks_x = max(pointarray[i][0][0],pointarray[i][1][0],pointarray[i][2][0])
        min_x = min(pointarray[i][0][0],pointarray[i][1][0],pointarray[i][2][0])
        maks_y = max(pointarray[i][0][1],pointarray[i][1][1],pointarray[i][2][1])
        min_y = min(pointarray[i][0][1],pointarray[i][1][1],pointarray[i][2][1])
        maks_z = max(pointarray[i][0][2],pointarray[i][1][2],pointarray[i][2][2])
        min_z = min(pointarray[i][0][2],pointarray[i][1][2],pointarray[i][2][2])

        sredina_x = (maks_x - min_x)/2 + min_x
        sredina_y = (maks_y - min_y)/2 + min_y
        sredina_z = (maks_z - min_z)/2 + min_z

        #odredivanje vektora prema izvoru
        Lx = izvor[0] - sredina_x
        Ly = izvor[1] - sredina_y
        Lz = izvor[2] - sredina_z

        #normalizacija vektora prema izvoru
        Ln = np.sqrt(np.power(Lx,2) + np.power(Ly,2) + np.power(Lz,2))
        Lx = Lx / Ln
        Ly = Ly / Ln
        Lz = Lz / Ln

        #normalizacija normale na povrsinu
        Nn = np.sqrt(np.power(normalarray[i][0],2) + np.power(normalarray[i][1],2) + np.power(normalarray[i][2],2))
        Nx = normalarray[i][0] / Nn
        Ny = normalarray[i][1] / Nn
        Nz = normalarray[i][2] / Nn

        LN = Lx * Nx + Ly * Ny + Lz * Nz

        #difuzna komponenta
        dif = Ii * kd * LN 
        if(dif < 0):
            dif = 0
        I = Ia * ka + dif
        glBegin(GL_TRIANGLES)
        glColor3ub(int(I), 0, 0)
        glVertex3f(pointarray[i][0][0],pointarray[i][0][1],pointarray[i][0][2])
        glVertex3f(pointarray[i][1][0],pointarray[i][1][1],pointarray[i][1][2])
        glVertex3f(pointarray[i][2][0],pointarray[i][2][1],pointarray[i][2][2])
        glEnd();


def trazi(param):
    param = list(param)
    k = 0
    for v in vertices:
        if(list(v) == param):
            return k
        k = k + 1
    
def Gouraud():
    privremeni = []
    nenormirani = []
    normirani = []
    vektor_normale = []

    Ia = 256
    ka = 0.3
    Ii = 256
    kd = 0.78125

    vertices_number = len(vertices)

    #nenormirani = lista s listama nenormiranih normala koje utjecu na pojedini vrh
    for i in range(1,vertices_number + 1):
        k = -1
        for f in faces:
            k = k + 1
            if(i in f):
                privremeni.append(G_normalarray[k])
                #print(str(i) + " " + str(f))
        nenormirani.append(privremeni)
        privremeni = []

    #normiranje svih normala
    for i in nenormirani:
        for j in i:
            Nn = np.sqrt(np.power(j[0],2) + np.power(j[1],2) + np.power(j[2],2))
            Nx = j[0] / Nn
            Ny = j[1] / Nn
            Nz = j[2] / Nn
            privremeni.append([Nx,Ny,Nz])
        normirani.append(privremeni)
        privremeni = []

    #normirani = normirane normale koje utjecu na pojedini vrh

    nvx = 0
    nvy = 0
    nvz = 0
    for i in normirani:
        broj = len(i)
        for j in i:
            nvx = nvx + j[0]
            nvy = nvy + j[1]
            nvz = nvz + j[2]
        vektor_normale.append([nvx/broj,nvy/broj,nvz/broj])
        nvx = 0
        nvy = 0
        nvz = 0

    for i in range(0,len(G_pointarray)):

        glBegin(GL_TRIANGLES)
        #prvi vrh

        #odredivanje vektora prema izvoru
        Lx = izvor[0] - G_pointarray[i][0][0]
        Ly = izvor[1] - G_pointarray[i][0][1]
        Lz = izvor[2] - G_pointarray[i][0][2]

        #normalizacija vektora prema izvoru
        Ln = np.sqrt(np.power(Lx,2) + np.power(Ly,2) + np.power(Lz,2)) 
        Lx = Lx / Ln
        Ly = Ly / Ln
        Lz = Lz / Ln

        #print(pointarray[i][0])
        #dohvacanje odgovarajuce normale
        indeks = trazi(G_pointarray[i][0])
        trazena_normala = vektor_normale[indeks]

        LN = Lx * trazena_normala[0] + Ly * trazena_normala[1] + Lz * trazena_normala[2]

        #difuzna komponenta
        dif = Ii * kd * LN 
        if(dif < 0):
            dif = 0
        I = Ia * ka + dif

        point1 = G_pointarray[i][0]
        point2 = G_pointarray[i][1]
        point3 = G_pointarray[i][2]

        normal = np.cross(point2-point1,point3-point1)

        if(np.dot(ociste,normal) > 0):
            glColor3ub(int(I),0,0)
            glVertex3f(G_pointarray[i][0][0],G_pointarray[i][0][1],G_pointarray[i][0][2])

        #drugi vrh

        #odredivanje vektora prema izvoru
        Lx = izvor[0] - G_pointarray[i][1][0]
        Ly = izvor[1] - G_pointarray[i][1][1]
        Lz = izvor[2] - G_pointarray[i][1][2]

        #normalizacija vektora prema izvoru
        Ln = np.sqrt(np.power(Lx,2) + np.power(Ly,2) + np.power(Lz,2)) 
        Lx = Lx / Ln
        Ly = Ly / Ln
        Lz = Lz / Ln

        #dohvacanje odgovarajuce normale
        indeks = trazi(G_pointarray[i][1])
        trazena_normala = vektor_normale[indeks]


        LN = Lx * trazena_normala[0] + Ly * trazena_normala[1] + Lz * trazena_normala[2]

        #difuzna komponenta
        dif = Ii * kd * LN 
        if(dif < 0):
            dif = 0
        I = Ia * ka + dif

        point1 = G_pointarray[i][0]
        point2 = G_pointarray[i][1]
        point3 = G_pointarray[i][2]

        normal = np.cross(point2-point1,point3-point1)

        if(np.dot(ociste,normal) > 0):
            glColor3ub(int(I),0,0)
            glVertex3f(G_pointarray[i][1][0],G_pointarray[i][1][1],G_pointarray[i][1][2])


        #treci vrh

        #odredivanje vektora prema izvoru
        Lx = izvor[0] - G_pointarray[i][2][0]
        Ly = izvor[1] - G_pointarray[i][2][1]
        Lz = izvor[2] - G_pointarray[i][2][2]

        #normalizacija vektora prema izvoru
        Ln = np.sqrt(np.power(Lx,2) + np.power(Ly,2) + np.power(Lz,2)) 
        Lx = Lx / Ln
        Ly = Ly / Ln
        Lz = Lz / Ln

        #print(pointarray[i][0])
        #dohvacanje odgovarajuce normale
        indeks = trazi(G_pointarray[i][2])
        trazena_normala = vektor_normale[indeks]

        LN = Lx * trazena_normala[0] + Ly * trazena_normala[1] + Lz * trazena_normala[2]

        #difuzna komponenta
        dif = Ii * kd * LN 
        if(dif < 0):
            dif = 0
        I = Ia * ka + dif

        point1 = G_pointarray[i][0]
        point2 = G_pointarray[i][1]
        point3 = G_pointarray[i][2]

        normal = np.cross(point2-point1,point3-point1)

        if(np.dot(ociste,normal) > 0):
            glColor3ub(int(I),0,0)
            glVertex3f(G_pointarray[i][2][0],G_pointarray[i][2][1],G_pointarray[i][2][2])

        glEnd()

if __name__ == "__main__":
    load_body()
    pyglet.app.run()