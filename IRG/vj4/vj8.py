from OpenGL.GL import *
from OpenGL.GLUT import *

window = 0

eps          = 100
m            = 16
umin,umax    = -1,1
vmin,vmax    = -1.2,1.2
width,height = 1920,1080
julia        = 1
if (julia != 0):
    c = 0.32 + 1j * 0.043
else:
    c = 0

def funk():
    global c
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    refresh2d(width, height)
    glClearColor(1.0, 1.0, 1.0, 1.0)
    xy_grid = [(x, y) for x in range(width) for y in range(height)]
    glBegin(GL_POINTS)
    for x0, y0 in xy_grid:
        u0 = (umax - umin) * x0 / float(width) + umin
        v0 = (vmax - vmin) * y0 / float(height) + vmin
        if (julia == 0):
            c = u0 + 1j * v0
            k, z0, r = -1, 0, 0
        else:
            z0 = u0 + 1j * v0
            k,r = -1, 0
        while (r < (eps*eps) and k < m):
            k = k + 1
            z0 = pow(z0, 2) + c
            r = (pow(z0.imag, 2) + pow(z0.real, 2))
        glColor3f(k/float(m), float(1-k)/(2*m), 0.8-k/(3*m) )
        glVertex2f(x0,y0)
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
window = glutCreateWindow("Vjezba 8: Fraktali")
glutDisplayFunc(funk)
glutMainLoop()
