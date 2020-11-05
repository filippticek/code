import fileinput
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
from math import *

window = 0
width, height = 800, 800
data      = fileinput.input("bird.obj")
inputfile = open('input')
pov       = list(tuple(map(float,inputfile.readline().split(" "))))
viewpoint = list(tuple(map(float,inputfile.readline().split(" "))))

verts   = []
polys   = []


for row in data:
    erow = row.split(" ")
    if 'v' in row:
        verts.append([float(erow[1]),float(erow[2]),float(erow[3])])
    elif 'f' in row:
        polys.append([int(erow[1]),int(erow[2]),int(erow[3])])

def transform(vp,pov,vert):
    t1   = np.mat([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [-vp[0], vp[1], -vp[2], 1]])
    g1   = np.dot(np.mat([pov[0], pov[1], pov[2], 1]), t1)
    sina = 0 if g1.item(0)==0 and g1.item(1)==0 else  g1.item(1) / sqrt(pow(g1.item(0), 2) + pow(g1.item(1), 2))
    cosa = 0 if g1.item(0)==0 and g1.item(1)==0 else  g1.item(0) / sqrt(pow(g1.item(0), 2) + pow(g1.item(1), 2))
    t2 = np.mat([[cosa, -sina, 0, 0], [sina, cosa, 0, 0],[0, 0, 1, 0], [0, 0, 0, 1]])
    g2 = np.dot(g1, t2)
    sinb = 0 if g2.item(0) == 0 and g2.item(2) == 0 else  g2.item(0) / sqrt(pow(g2.item(0), 2) + pow(g2.item(2), 2))
    cosb = 0 if g2.item(0) == 0 and g2.item(2) == 0 else  g2.item(2) / sqrt(pow(g2.item(0), 2) + pow(g2.item(2), 2))
    t3 = np.mat([[cosb, 0, sinb, 0], [0, 1, 0, 0],[-sinb, 0, cosb, 0], [0, 0, 0, 1]])
    g3 = np.dot(g2,t3)
    t4 = np.mat([[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 1, 0],[0, 0, 0, 1]])
    t5 = np.mat([[-1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0],[0, 0, 0, 1]])
    t  = np.dot(np.dot(np.dot(np.dot(t1,t2),t3),t4),t5)
    p  = np.mat([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1/g3.item(2)], [0, 0, 0, 0]])
    x  = vert[0]
    y  = vert[1]
    z  = vert[2]
    ver= np.dot(np.dot(np.mat([x,y,z,1]),t),p)
    ht = ver.item(3)
    if ht != 1 and ht != 0:
        ver = [ver.item(0) / ht, ver.item(1) / ht, ver.item(2) / ht, ver.item(3) / ht]
    else:
        ver = [ver.item(0) ,ver.item(1), ver.item(2), ver.item(3)]
    return ver

def enlarge(vert,n):
    return [vert[0]*n+300.0,vert[1]*n+300.0, 0, 1]
 

def funk():
    global verts,width,height, viewpoint,pov
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    refresh2d(width, height)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glColor3f(1.0, 1.0, 1.0)
    for i in range(0,len(polys)):
        v1 = transform(viewpoint,pov, verts[polys[i][0] - 1])
        v2 = transform(viewpoint,pov, verts[polys[i][1] - 1])
        v3 = transform(viewpoint,pov, verts[polys[i][2] - 1])
        #print v1
        #print v2
        #print v3
        v1 = enlarge(v1,100.0)
        v2 = enlarge(v2,100.0)
        v3 = enlarge(v3,100.0)
        glBegin(GL_LINE_LOOP)
        glVertex3f(v1[0],v1[1],0)
        glVertex3f(v2[0],v2[1],0)
        glVertex3f(v3[0],v3[1],0)
        glEnd()
    glutSwapBuffers()

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def redisplay_all():
    glutSetWindow(window)
    refresh2d(width, height)
    glutPostRedisplay()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
glutInitWindowSize(width, height)
glutInitWindowPosition(100, 100)
window = glutCreateWindow("Vjezba 5")
glutReshapeFunc(refresh2d)
glutDisplayFunc(funk)
redisplay_all()
glutMainLoop()

