from OpenGL.GL import *
from OpenGL.GLU import *


def main():
    dlWorld = glGenLists(1)
    glNewList(dlWorld, GL_COMPILE)
    #Draw Axes
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(1,0,0); glVertex3i(0,0,0); glVertex3i(  0, 100,  0)
    glColor3f(1,1,0); glVertex3i(0,0,0); glVertex3i(100, 0  ,  0)
    glColor3f(0,0,1); glVertex3i(0,0,0); glVertex3i(  0, 0  ,100)
    glEnd()
    glColor3f(1,1,1)
##    #Draw XZ Plane
##    glBegin(GL_QUADS)
##    glTexCoord2i(0,1);glVertex3i(0,0,0)
##    glTexCoord2i(1,1);glVertex3i(100,0,0)
##    glTexCoord2i(1,0);glVertex3i(100,0,100)
##    glTexCoord2i(0,0);glVertex3i(0,0,100)
##    glEnd()
    glEndList()

    dlRotatedAxes = glGenLists(1)
    glNewList(dlRotatedAxes, GL_COMPILE)
    #Draw Axes
    glLineWidth(3)
    glBegin(GL_LINES)
    glColor3f(1.0,0.5,0.5); glVertex3i(0,0,0); glVertex3i(  0, 100,  0)
    glColor3f(1.0,1.0,0.5); glVertex3i(0,0,0); glVertex3i(100, 0  ,  0)
    glColor3f(0.5,0.5,1.0); glVertex3i(0,0,0); glVertex3i(  0, 0  ,100)
    glEnd()
    glColor3f(1,1,1)
    glEndList()

    dlSphere = glGenLists(1)
    glNewList(dlSphere, GL_COMPILE)
    Sphere = gluNewQuadric()
    gluSphere(Sphere, 1, 20, 20)
    glEndList()
    
    return [dlWorld,dlRotatedAxes,dlSphere]
