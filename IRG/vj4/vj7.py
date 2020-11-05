from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import math
import sys

class Tocka:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

ociste = Tocka(1.0, -1.0, 3.0)
glediste = Tocka(0, 0, 0)
izvor = Tocka(2, 5, 2)

metoda = 2  # 1-wire, 2-konst, 3-gouraud

Ia = 100
ka = 0.5

Ii = 200
kd = 0.5

window = []
width = 600
height = 600

vrhovi = []
poligoni = []

normale = []
normalevrhova = []
ravnine = []
sredistapoligona = []

intenzitetivrhova = []
intenzitetipoligona = []


# funkcija display, poziva se konstantno
# ona poziva i sjencanje
def mydisplay():
    # brise zaslon
    glClearColor(1.0, 1.0, 1.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # radnja koja se izvrsava
    if metoda == 1:
        myobject()
    if metoda == 2:
        konstantno()
    if metoda == 3:
        gouraud()

    # clear-a buffer
    glutSwapBuffers()
    
# funkcija koja se poziva pri promjeni dimenzija prozora
def myreshape(w, h):

    global window
    global width
    global height

    # azuriraj vrijednosti dimenzija prozora
    width = w
    height = h

    # view postaviti na vrijednosti dimenzija prozora
    glViewport(0, 0, width, height)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(width / height), 0.5, 15.0)
    gluLookAt(ociste.x, ociste.y, ociste.z, glediste.x, glediste.y, glediste.z, 0.0, 1.0, 0.0)

    # vratiti na model view
    glMatrixMode(GL_MODELVIEW)

# crtanje wireframe-a (3. lab vjezba)
def myobject():
    for i in range(0, len(poligoni)):

        if nevidljiv(i):
            glBegin(GL_LINE_LOOP)
            v1 = vrhovi[int(poligoni[i][0]) - 1]
            v2 = vrhovi[int(poligoni[i][1]) - 1]
            v3 = vrhovi[int(poligoni[i][2]) - 1]

            glColor3ub(255, 0, 0)
            glVertex3f(v1[0], v1[1], v1[2])
            glColor3ub(255, 0, 0)
            glVertex3f(v2[0], v2[1], v2[2])
            glColor3ub(255, 0, 0)
            glVertex3f(v3[0], v3[1], v3[2])

            glEnd()

# konstantno sjencanje
def konstantno():
    global intenzitetipoligona

    for i in range(0, len(poligoni)):
        if nevidljiv(i):
            glBegin(GL_TRIANGLES)
            v1 = vrhovi[int(poligoni[i][0]) - 1]
            v2 = vrhovi[int(poligoni[i][1]) - 1]
            v3 = vrhovi[int(poligoni[i][2]) - 1]

            glColor3ub(int(intenzitetipoligona[i]), 0, 0)
            glVertex3f(v1[0], v1[1], v1[2])
            glColor3ub(int(intenzitetipoligona[i]), 0, 0)
            glVertex3f(v2[0], v2[1], v2[2])
            glColor3ub(int(intenzitetipoligona[i]), 0, 0)
            glVertex3f(v3[0], v3[1], v3[2])

            glEnd()

# gouraud-ovo sjencanje
def gouraud():
    global intenzitetivrhova

    for i in range(0, len(poligoni)):
        if nevidljiv(i):
            glBegin(GL_TRIANGLES)
            v1 = vrhovi[int(poligoni[i][0]) - 1]
            v2 = vrhovi[int(poligoni[i][1]) - 1]
            v3 = vrhovi[int(poligoni[i][2]) - 1]

            i1 = intenzitetivrhova[int(poligoni[i][0]) - 1]
            i2 = intenzitetivrhova[int(poligoni[i][1]) - 1]
            i3 = intenzitetivrhova[int(poligoni[i][2]) - 1]

            glColor3ub(i1, 0, 0)
            glVertex3f(v1[0], v1[1], v1[2])
            glColor3ub(i2, 0, 0)
            glVertex3f(v2[0], v2[1], v2[2])
            glColor3ub(i3, 0, 0)
            glVertex3f(v3[0], v3[1], v3[2])

            glEnd()

# je li poligon vidljiv ili ne
def nevidljiv(i):
    vektor = [ociste.x - sredistapoligona[i][0], ociste.y - sredistapoligona[i][1], ociste.z - sredistapoligona[i][2]]

    d = math.sqrt(vektor[0] * vektor[0] + vektor[1] * vektor[1] + vektor[2] * vektor[2])
    brojnik = (vektor[0] / d) * ravnine[i][0] + (vektor[1] / d) * ravnine[i][1] + (vektor[2] / d) * ravnine[i][2]

    if brojnik > 0:
        return 1
    else:
        return 0

# ucitava tijelo iz datoteke
def ucitajtijelo():
    finput = open('bird.obj', 'r')
    ulaz = finput.readlines()

    global vrhovi
    global poligoni

    for each in ulaz:
        each = each.rstrip()
        if each == "":
            continue
        if each[0] == 'v':
            each = each.split()
            each.pop(0)
            vrhovifloat = []
            for v in each:
                vrhovifloat.append(float(v))
            vrhovi.append(vrhovifloat)
        elif each[0] == 'f':
            each = each.split()
            each.pop(0)
            poligoni.append(each)
        else:
            continue

# pomaknuti / skalirati tijelo na sred ekranskog prikaza
def smjestitijelo():
    global vrhovi

    xmax = -sys.maxsize
    xmin = sys.maxsize

    ymax = -sys.maxsize
    ymin = sys.maxsize

    zmax = -sys.maxsize
    zmin = sys.maxsize

    # popuni ih
    for vrh in vrhovi:
        if vrh[0] > xmax:
            xmax = vrh[0]
        if vrh[0] < xmin:
            xmin = vrh[0]
        if vrh[1] > ymax:
            ymax = vrh[1]
        if vrh[1] < ymin:
            ymin = vrh[1]
        if vrh[2] > zmax:
            zmax = vrh[2]
        if vrh[2] < zmin:
            zmin = vrh[2]

    # izracunati dimenzije tijela na temelju min/max vrijednosti
    velicina_x = xmax - xmin
    velicina_y = ymax - ymin
    velicina_z = zmax - zmin

    # izracunati srediste tijela na temelju dimenzija
    srediste_x = (xmax + xmin) / 2
    srediste_y = (ymax + ymin) / 2
    srediste_z = (zmax + zmin) / 2

    # odrediti kojim faktorom mnoziti
    faktor = max(velicina_x, velicina_y, velicina_z)

    # pomaknuti tijelo u srediste
    for vrh in vrhovi:
        vrh[0] -= srediste_x
        vrh[1] -= srediste_y
        vrh[2] -= srediste_z

    # skalirati tijelo na ekran
    for vrh in vrhovi:
        vrh[0] *= (2 / faktor)
        vrh[1] *= (2 / faktor)
        vrh[2] *= (2 / faktor)

def izracunajABCD():

    global ravnine
    global poligoni
    global vrhovi
    global normale
    global sredistapoligona

    for every in poligoni:

        # odrediti 3 vrha svakog poligona (trokuta)
        # oduzeti 1 po definiciji .obj datoteke
        v1 = vrhovi[int(every[0]) - 1]
        v2 = vrhovi[int(every[1]) - 1]
        v3 = vrhovi[int(every[2]) - 1]

        # odrediti maksimalne vrijednost
        xmax = max(v1[0], v2[0], v3[0])
        ymax = max(v1[1], v2[1], v3[1])
        zmax = max(v1[2], v2[2], v3[2])

        # odrediti minimalne vrijednosti
        xmin = min(v1[0], v2[0], v3[0])
        ymin = min(v1[1], v2[1], v3[1])
        zmin = min(v1[2], v2[2], v3[2])

        # srediste poligona
        sredisnja = [(xmax + xmin) / 2, (ymax + ymin) / 2, (zmax + zmin) / 2]
        sredistapoligona.append(sredisnja)

        # odrediti ravnine poligona
        A =  (float(v2[1]) - float(v1[1])) * (float(v3[2]) - float(v1[2])) - (float(v2[2]) - float(v1[2])) * (float(v3[1]) - float(v1[1]))
        B = -(float(v2[0]) - float(v1[0])) * (float(v3[2]) - float(v1[2])) + (float(v2[2]) - float(v1[2])) * (float(v3[0]) - float(v1[0]))
        C =  (float(v2[0]) - float(v1[0])) * (float(v3[1]) - float(v1[1])) - (float(v2[1]) - float(v1[1])) * (float(v3[0]) - float(v1[0]))
        D = -A * float(v1[0]) - B * float(v1[1]) - C * float(v1[2])
        ravnine.append((A, B, C, D))

        # normalizirane norme poligona
        tmp = math.sqrt(A**2 + B**2 + C**2)
        normale.append((A/tmp, B/tmp, C/tmp))

def racunajintenzitetepoligona():
    global intenzitetipoligona

    for i in range(0, len(poligoni)):
        # odredi udaljenost izvora
        l = [izvor.x - sredistapoligona[i][0],
             izvor.y - sredistapoligona[i][1],
             izvor.z - sredistapoligona[i][2]]

        lsqrt = math.sqrt(l[0]**2 + l[1]**2 + l[2]**2)
        lnorm = [l[0] / lsqrt, l[1] / lsqrt, l[2] / lsqrt]

        intenzitetipoligona.append(math.floor(
            Ia * ka + Ii * kd * (lnorm[0] * normale[i][0] + lnorm[1] * normale[i][1] + lnorm[2] * normale[i][2])))

# izracunati normale vrhove na temelju normala okolnih poligona
def racunajnormalevrhova():
    global normalevrhova

    normalevrhova = []
    for i in range(1, len(vrhovi) + 1):
        normV = []

        for j in range(0, len(poligoni)):
            if str(i) in poligoni[j]:
                normV.append(normale[j])

        # prema normalama okolnih poligona, odrediti normalu vrha
        n_x = 0
        n_y = 0
        n_z = 0
        for each in normV:
            n_x += each[0]
            n_y += each[1]
            n_z += each[2]

        # koliko poligona dijeli ovaj vrh
        n_x /= len(normV)
        n_y /= len(normV)
        n_z /= len(normV)

        # normalizirati
        nlen = math.sqrt(n_x**2 + n_y**2 + n_z**2)
        normalevrhova.append((n_x / nlen, n_y / nlen, n_z / nlen))

# izracunati intenzitete vrhova, prema formuli
def racunajintenzitetevrhova():
    global intenzitetivrhova

    for i in range(0, len(vrhovi)):
        l = [izvor.x - vrhovi[i][0], izvor.y - vrhovi[i][1], izvor.z - vrhovi[i][2]]
        lsqrt = math.sqrt(l[0] * l[0] + l[1] * l[1] + l[2] * l[2])
        lnorm = [l[0] / lsqrt, l[1] / lsqrt, l[2] / lsqrt]

        intenzitetivrhova.append(int(Ia * ka + Ii * kd * (lnorm[0] * normalevrhova[i][0] + lnorm[1] * normalevrhova[i][1] + lnorm[2] * normalevrhova[i][2])))

def redisplay_all():
    glutSetWindow(window)
    myreshape(width, height)
    glutPostRedisplay()

glutInit(sys.argv)
# setup ekrana
glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH)
glutInitWindowSize(width, height)
glutInitWindowPosition(100, 100)
window = glutCreateWindow("Vjezba 7.")
glEnable(GL_DEPTH_TEST)
glDepthFunc(GL_LEQUAL)
# postavke funkcija koje se pozivaju
glutReshapeFunc(myreshape)
glutDisplayFunc(mydisplay)
# zadaci sa labosa
ucitajtijelo()
smjestitijelo()
izracunajABCD()
racunajintenzitetepoligona()
racunajnormalevrhova()
racunajintenzitetevrhova()
redisplay_all()
glutMainLoop()
