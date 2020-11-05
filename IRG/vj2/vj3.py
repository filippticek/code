from OpenGL.GL import *
from OpenGL.GLUT import *

window = 0
width, height = 500, 500
vList = []

#n = int(input("Koliko tocaka?: "))
#for vert in range(1,n+1):
#    msg = "Vrh poligona " + str(vert) + ": "
#    vList.append(list(tuple(map(int,str(input(msg)).split(" ")))))
#point = list(tuple(map(int,str(input("Tocka: ")).split(" "))))

inputfile = open('input')

n = int(inputfile.readline())

for vert in range(1,n+1):
	vList.append(list(tuple(map(int, inputfile.readline().split(" ")))))
point = list(tuple(map(int, inputfile.readline().split(" "))))

xmax = vList[0][0]
ymax = vList[0][1]
xmin = vList[0][0]
ymin = vList[0][1]
for vert in vList:
    if vert[0] > xmax:
        xmax = vert[0]
    if vert[0] < xmin:
        xmin = vert[0]
    if vert[1] > ymax:
        ymax = vert[1]
    if vert[1] < ymin:
        ymin = vert[1]

coefs = []
for i in range(0,n):
    xi = vList[i][0]
    yi = vList[i][1]
    if i != n-1:
        xi1 = vList[i+1][0]
        yi1 = vList[i+1][1]
    else:
        xi1 = vList[0][0]
        yi1 = vList[0][1]
    a = yi - yi1
    b = -xi + xi1
    c = xi * yi1 - xi1 * yi
    coefs.append([a,b,c])

out = 0
for abc in coefs:
    val = point[0] * abc[0] + point[1] * abc[1] + abc[2]
    if val > 0:
        out = 1

if out == 1:
    print("Tocka je izvan poligona")
else:
    print("Tocka je unutar poligona")

def funk():
    global xmin,xmax,ymin,ymax,coefs,vList,width,height,n
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    refresh2d(width, height)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glColor3f(1.0, 0.0, 0.0)
#crtaj poligon
    for i in range(0,n):
        if i == n-1:
            glBegin(GL_LINES)
            glVertex2i(vList[i][0], vList[i][1])
            glVertex2i(vList[0][0], vList[0][1])
            glEnd()
        else:
            glBegin(GL_LINES)
            glVertex2i(vList[i][0], vList[i][1])
            glVertex2i(vList[i+1][0], vList[i+1][1])
            glEnd()

#puni poligon
    for y0 in range(ymin,ymax):
        l = xmin
        d = xmax
        for i in range(0,n):
            if coefs[i][0] == 0:
                continue
            x = (-coefs[i][1] * y0 - coefs[i][2])/coefs[i][0]
            if i == n-1:
                yi1 = vList[0][1]
            else:
                yi1 = vList[i+1][1]
            yi = vList[i][1]
            if yi < yi1 and x > l:
                l = x
            if yi >= yi1 and x < d:
                d = x

        if l < d:
            glBegin(GL_LINES)
            glVertex2i(l, y0)
            glVertex2i(d, y0)
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
window = glutCreateWindow("Vjezba 3: Poligon")
glutDisplayFunc(funk)
glutMainLoop()
