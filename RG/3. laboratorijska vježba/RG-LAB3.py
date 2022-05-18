from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from math import * 
from NiaPy.task import StoppingTask, OptimizationType
from NiaPy.benchmarks import Benchmark
from NiaPy.algorithms.basic import ParticleSwarmAlgorithm
from NiaPy.task import StoppingTask

w,h= 500,500

colour_list = []

def snowman():
    global colour_list
    posx, posy = 250,127    
    sides = 32    
    radius = 100
    #donji dio
    glBegin(GL_POLYGON) 
    r,g,b = colouring(colour_list[2])
    glColor3f(r,g,b)   
    #glColor3f(21.0, 159.0, 0.0)  

    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + posx    
        sine  = radius * sin(i*2*pi/sides) + posy    
        glVertex2f(cosine,sine)
    glEnd()

    #desna ruka
    glBegin(GL_TRIANGLES)
    #glColor3f(1.0, 1.0, 0.0)
    r,g,b = colouring(colour_list[12])
    glColor3f(r,g,b)   
    glVertex2f(270,335)
    glVertex2f(390,380)
    glVertex2f(320,310)
    glEnd()

    #lijeva ruka
    glBegin(GL_TRIANGLES)
    #glColor3f(1.0, 1.0, 0.0)
    r,g,b = colouring(colour_list[11])
    glColor3f(r,g,b)   
    glVertex2f(250,335)
    glVertex2f(110,380)
    glVertex2f(180,310)
    glEnd()

    #kapa
    glBegin(GL_TRIANGLES)
    #glColor3f(1.0, 1.0, 0.0)
    r,g,b = colouring(colour_list[3])
    glColor3f(r,g,b)   
    glVertex2f(240,473)
    glVertex2f(260,473)
    glVertex2f(250,498)
    glEnd()

    #srednji dio
    posx, posy = 250,300    
    sides = 32    
    radius = 75   
    glBegin(GL_POLYGON) 
    #glColor3f(255, 0, 0)
    r,g,b = colouring(colour_list[1])
    glColor3f(r,g,b)  
    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + posx    
        sine  = radius * sin(i*2*pi/sides) + posy    
        glVertex2f(cosine,sine)
    glEnd()

    #glava
    posx, posy = 250,423    
    sides = 32    
    radius = 50   
    glBegin(GL_POLYGON) 
    #glColor3f(0, 255, 0)
    r,g,b = colouring(colour_list[0])
    glColor3f(r,g,b)  
    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + posx    
        sine  = radius * sin(i*2*pi/sides) + posy    
        glVertex2f(cosine,sine)
    glEnd()

    # lijevo oko
    posx, posy = 230,440    
    sides = 32    
    radius = 10    
    glBegin(GL_POLYGON)
    r,g,b = colouring(colour_list[4])
    glColor3f(r,g,b) 
    #glColor3f(1.0, 1.0, 0.0)  
    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + posx    
        sine  = radius * sin(i*2*pi/sides) + posy    
        glVertex2f(cosine,sine)
    glEnd()

    #desno oko
    posx, posy = 270,440    
    sides = 32    
    radius = 10   
    glBegin(GL_POLYGON) 
    r,g,b = colouring(colour_list[5])
    #glColor3f(1.0, 1.0, 0.0)
    glColor3f(r,g,b)   
    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + posx    
        sine  = radius * sin(i*2*pi/sides) + posy    
        glVertex2f(cosine,sine)
    glEnd()

    posx, posy = 265,405    
    sides = 32    
    radius = 5   
    #glColor3f(1.0, 1.0, 0.0)
    glBegin(GL_POLYGON)
    r,g,b = colouring(colour_list[7]) 
    glColor3f(r,g,b) 
    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + posx    
        sine  = radius * sin(i*2*pi/sides) + posy    
        glVertex2f(cosine,sine)
    glEnd()

    posx, posy = 255,400    
    sides = 32    
    radius = 5   
    glBegin(GL_POLYGON) 
    #glColor3f(1.0, 1.0, 0.0) 
    r,g,b = colouring(colour_list[8])
    glColor3f(r,g,b)  
    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + posx    
        sine  = radius * sin(i*2*pi/sides) + posy    
        glVertex2f(cosine,sine)
    glEnd()

    posx, posy = 245,400    
    sides = 32    
    radius = 5   
    #glColor3f(1.0, 1.0, 0.0) 
    glBegin(GL_POLYGON)
    r,g,b = colouring(colour_list[9]) 
    glColor3f(r,g,b) 
    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + posx    
        sine  = radius * sin(i*2*pi/sides) + posy    
        glVertex2f(cosine,sine)
    glEnd()

    posx, posy = 235,405    
    sides = 32    
    radius = 5   
    glBegin(GL_POLYGON)
    r,g,b = colouring(colour_list[10])
    glColor3f(r,g,b) 
    #glColor3f(1.0, 1.0, 0.0)  
    for i in range(100):    
        cosine= radius * cos(i*2*pi/sides) + posx    
        sine  = radius * sin(i*2*pi/sides) + posy    
        glVertex2f(cosine,sine)
    glEnd()

    #nos
    glBegin(GL_TRIANGLES)
    #glColor3f(1.0, 1.0, 0.0)
    r,g,b = colouring(colour_list[6])
    glColor3f(r,g,b)   
    glVertex2f(250,415)
    glVertex2f(250,425)
    glVertex2f(225,419)
    glEnd()

def iterate():
    glViewport(0, 0, 500, 500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 500, 0.0, 500, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    snowman()
    glutSwapBuffers()

def map_shape_to_color(particle):
    col = []
    for i in range(len(particle)):
        if(particle[i] >= 0.0 and particle[i] < 0.1):
            col.append(1) # orange
        if(particle[i] >= 0.1 and particle[i] < 0.2):
            col.append(2) # black
        if(particle[i] >= 0.2 and particle[i] < 0.3):
            col.append(3) # blue
        if(particle[i] >= 0.3 and particle[i] < 0.4):
            col.append(4) # red
        if(particle[i] >= 0.4 and particle[i] < 0.5):
            col.append(5) # yellow
        if(particle[i] >= 0.5 and particle[i] < 0.6):
            col.append(6) # green
        if(particle[i] >= 0.6 and particle[i] < 0.7):
            col.append(7) # magenta
        if(particle[i] >= 0.7 and particle[i] < 0.8):
            col.append(8) # cyan
        if(particle[i] >= 0.8 and particle[i] < 0.9):
            col.append(9) # Maya Blue
        if(particle[i] >= 0.9 and particle[i] < 1.0):
            col.append(10) # coral
        if(particle[i] > 1.0):
            print("Colour can't be greater than 1.0!")
    return col

# one particle has this form: particle = (head, body, legs, hat, left_eye, right_eye, nose, mouth1, mouth2, mouth3, mouth4, left_hand, right_hand)
# head = particle[0]
# body = particle[1] 
# legs = particle[2]
# hat = particle[3] 
# left_eye = particle[4] 
# right_eye = particle[5] 
# nose = particle[6] 
# mouth1 = particle[7] 
# mouth2 = particle[8]
# mouth3 = particle[9] 
# mouth4 = particle[10] 
# left_hand = particle[11] 
# right_hand = particle[12]

def colouring(value):
    if(value == 1):
        # Orange
        r = 1
        g = 0.5
        b = 0
        return r,g,b
    if(value == 2):
        # Black
        r = 0
        g = 0
        b = 0
        return r,g,b
    if(value == 3):
        # Blue
        r = 0
        g = 0
        b = 1
        return r,g,b
    if(value == 4):
        # Red
        r = 1
        g = 0
        b = 0
        return r,g,b
    if(value == 5):
        # Yellow
        r = 1
        g = 1
        b = 0
        return r,g,b
    if(value == 6):
        # Green
        r = 0
        g = 1
        b = 0
        return r,g,b
    if(value == 7):
        # Magenta
        r = 1
        g = 0
        b = 1
        return r,g,b
    if(value == 8):
        # Cyan
        r = 0
        g = 1
        b = 1
        return r,g,b
    if(value == 9):
        # Maya Blue
        r = 0.49
        g = 0.73
        b = 0.91
        return r,g,b
    if(value == 10):
        # Coral
        r = 1
        g = 0.5
        b = 0.31
        return r,g,b

# number of colours must be greater or eaqual to 4
def constraint1(particle):
    if(len(set(particle)) >= 4):
        return 1
    else:
        return 0

# head colour and colour of the eyes must not be the same
def constraint2(particle):
    if(particle[0] != particle[4] and particle[0] != particle[5]):
        return 1
    else:
        return 0

# colours of the head and nose must not be the same
def constraint3(particle):
    if(particle[0] != particle[6]):
        return 1
    else:
        return 0

# mouth colour must be different than the head colour
def constraint4(particle):
    if(particle[0] != particle[7] and particle[0] != particle[8] and particle[0] != particle[9] and particle[0] != particle[10]):
        return 1
    else:
        return 0

# colour of the hat must not be black
def constraint5(particle):
    if(particle[3] != 2):
        return 1
    else:
        return 0

# head must not be orange or coral
def constraint6(particle):
    if(particle[0] != 10 and particle[0] != 1):
        return 1
    else:
        return 0

# head must not be the same color as hat
def constraint7(particle):
    if(particle[0] != particle[3]):
        return 1
    else:
        return 0

# our custom benchmark class
class MyBenchmark(Benchmark):
    def __init__(self):
        Benchmark.__init__(self, 0.0, 0.99) # search space dimensions

    def function(self):
        def evaluate(D, sol):
            val = 0

            sol = map_shape_to_color(sol)
            if(constraint1(sol) == 1): val += 1
            if(constraint2(sol) == 1): val += 1
            if(constraint3(sol) == 1): val += 1
            if(constraint4(sol) == 1): val += 1
            if(constraint5(sol) == 1): val += 1
            if(constraint6(sol) == 1): val += 1
            if(constraint7(sol) == 1): val += 1

            return val
        return evaluate


for i in range(1):
    task = StoppingTask(D = 13, nGEN = 100, optType = OptimizationType.MAXIMIZATION, benchmark = MyBenchmark())
 
    # parameter is population size
    algo = ParticleSwarmAlgorithm(NP = 13)

    # running algorithm returns best found maximum
    best = algo.run(task)

    # printing best minimum
    print(best[1])
    
    #printing the best solution
    print(best[0])

    #convert best solution found to colors
    print("Solution to color: ", map_shape_to_color(best[0]))
    colour_list = map_shape_to_color(best[0])


glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(500, 500)
glutInitWindowPosition(0, 0)
wind = glutCreateWindow("Racunalna grafika - 3. lab vjezba")
glClearColor( 1, 1, 1, 1)
glutDisplayFunc(showScreen)
glutIdleFunc(showScreen)
glutMainLoop()

