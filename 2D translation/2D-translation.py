from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

# Original triangle
triangle = [
    (1, 1),
    (5, 2),
    (3, 6)
]

# Translation values
tx = 4
ty = 3


def draw_triangle(points):
    glBegin(GL_LINE_LOOP)

    for x, y in points:
        glVertex2f(x, y)

    glEnd()


def display():
    glClear(GL_COLOR_BUFFER_BIT)

    # ---------------- ORIGINAL TRIANGLE ----------------
    glColor3f(1.0, 0.0, 0.0)

    draw_triangle(triangle)

    # ---------------- TRANSLATED TRIANGLE ----------------
    glPushMatrix()

    # Translation matrix
    glTranslatef(tx, ty, 0)

    glColor3f(0.0, 1.0, 0.0)

    draw_triangle(triangle)

    glPopMatrix()

    glFlush()


def init():
    glClearColor(1.0, 1.0, 1.0, 1.0)

    # Coordinate system
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluOrtho2D(-2, 12, -2, 12)

    glMatrixMode(GL_MODELVIEW)


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)

glutInitWindowSize(700, 700)
glutInitWindowPosition(100, 100)

glutCreateWindow(b"2D Translation")

init()

glutDisplayFunc(display)

glutMainLoop()