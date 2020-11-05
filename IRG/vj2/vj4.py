import fileinput
from OpenGL.GL import *
from OpenGL.GLUT import *

window = 0
width, height = 800, 800
data = fileinput.input("teapot.obj")
point = [.5,0.5,0.5]
verts = []
polys = []
coefs = []

for row in data:
    erow = row.split(" ")
    if '#' in row or 'g' in row:
		continue
    if 'v' in row:
        verts.append([float(erow[1]),float(erow[2]),float(erow[3])])
    elif 'f' in row:
        polys.append([int(erow[1]),int(erow[2]),int(erow[3])])

for poly in polys:
    v1 = verts[poly[0]-1]
    v2 = verts[poly[1]-1]
    v3 = verts[poly[2]-1]
    a  = (v2[1]-v1[1])*(v3[2]-v1[2])-(v2[2]-v1[2])*(v3[1]-v1[1])
    b  = -(v2[0]-v1[0])*(v3[2]-v1[2])+(v2[2]-v1[2])*(v3[0]-v1[0])
    c  = (v2[0]-v1[0])*(v3[1]-v1[1])-(v2[2]-v1[2])*(v3[0]-v1[0])
    d  = -v1[0]*a - v1[1]*b - v1[2]*c
    coefs.append([a,b,c,d])

out = 0
for abc in coefs:
    val = point[0]*abc[0] + point[1]*abc[1] + point[2]*abc[2] + abc[3]
    if val > 0:
        out = 1

if out == 1:
    print("Tocka je izvan tijela")
else:
    print("Tocka je unutar tijela")

def enlarge(verts,n):
    for i in range(0,len(verts)):
        verts[i] = [verts[i][0]*n+400.0,verts[i][1]*n+400.0,verts[i][2]*n]
    return verts

def funk():
    global verts,width,height
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    refresh2d(width, height)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glColor3f(1.0, 1.0, 1.0)
#crtaj poligone
    verts = enlarge(verts, 100.0)
    for i in range(0,len(polys)):
        v1 = verts[polys[i][0] - 1]
        v2 = verts[polys[i][1] - 1]
        v3 = verts[polys[i][2] - 1]
        glBegin(GL_LINE_LOOP)
        glVertex3f(v1[0], v1[1], 0)
        glVertex3f(v2[0], v2[1], 0)
        glVertex3f(v3[0], v3[1], 0)
        glEnd()
    glutSwapBuffers()

def refresh2d(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, width, 0.0, height, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

glutInit()
glutInitDisplayMode(GLUT_RGBA | GLUT_SINGLE)
glutInitWindowSize(width, height)
glutInitWindowPosition(100, 100)
window = glutCreateWindow("Vjezba 4: Objekti")
glutDisplayFunc(funk)
glutMainLoop()
