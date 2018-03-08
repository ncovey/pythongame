from OpenGL.GL import *
from OpenGL.GLU import *
import os, sys, math, random
from numpy import *
import pygame
from pygame.locals import *
if sys.platform == 'win32' or sys.platform == 'win64':
    os.environ['SDL_VIDEO_CENTERED'] = '1'
import gl, objects

pygame.init()

screen_size = (800,600)
icon = pygame.Surface((1,1))
icon.set_alpha(0)
pygame.display.set_icon(icon)
pygame.display.set_caption("3D Rotations Demo - v.2.0.1 - Ian Mallett - 2018")
pygame.display.set_mode(screen_size,OPENGL|DOUBLEBUF)
gl.resize(*screen_size)
gl.init()

Objects = objects.main()
dlWorld       = Objects[0]
dlRotatedAxes = Objects[1]
dlSphere      = Objects[2]

CameraPos = [65.6,140.0,216.0]
CameraRotate = [-10,-30]

Points = [[50,50,50]]
Rotations = [0.0,0.0,0.0] #Y AXIS, X AXIS, Z AXIS

print("Use the a and s keys to rotate around the y (up/down) axis.")
print("Use the UP and DOWN keys to rotate the coordinate system up or down.")
print("Use the LEFT and RIGHT keys to rotate the coordinates system left and right.")

def GetPoint(Point):
    #Basic position
    X = 0.0
    Y = 0.0
    Z = 0.0
    #Fancy Matrix Stuff - WOW!
    A = math.radians(Rotations[0])
    B = math.radians(Rotations[1])
    G = math.radians(Rotations[2])
    AlphaRotationMatrix = matrix([[  math.cos(A),  math.sin(A),  0.0        ],
                                  [ -math.sin(A),  math.cos(A),  0.0        ],
                                  [  0.0        ,  0.0        ,  1.0        ]])
    BetaRotationMatrix  = matrix([[  1.0        ,  0.0        ,  0.0        ],
                                  [  0.0        ,  math.cos(B),  math.sin(B)],
                                  [  0.0        , -math.sin(B),  math.cos(B)]])
    GammaRotationMatrix = matrix([[  math.cos(G),  math.sin(G),  0.0        ],
                                  [ -math.sin(G),  math.cos(G),  0.0        ],
                                  [  0.0        ,  0.0        ,  1.0        ]])
    ProductMatrix        = AlphaRotationMatrix*BetaRotationMatrix*GammaRotationMatrix
    x = 0
    y = 2
    z = 1
    PositionVectorMatrix = matrix([[Point[x]],[Point[y]],[Point[z]]])
    PositionMatrix       = ProductMatrix*PositionVectorMatrix
    X += PositionMatrix[x][0]
    Y += PositionMatrix[y][0]
    Z += PositionMatrix[z][0]
    return [X,Y,Z]
def GetInput():
    global CameraPos, CameraRotate
    global Rotations
    keystate = pygame.key.get_pressed()
    mrel = pygame.mouse.get_rel()
    mpress = pygame.mouse.get_pressed()
    for event in pygame.event.get():
        if event.type == QUIT or keystate[K_ESCAPE]:
            pygame.quit(); sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            ScrollSpeed = 5
            if event.button == 4: #Scroll In
                CameraPos[1] += ScrollSpeed*math.sin(math.radians(CameraRotate[1]))
                CameraPos[2] -= ScrollSpeed*math.cos(math.radians(CameraRotate[0]))*math.cos(math.radians(CameraRotate[1]))
                CameraPos[0] += ScrollSpeed*math.sin(math.radians(CameraRotate[0]))*math.cos(math.radians(CameraRotate[1]))
            elif event.button == 5: #Scroll Out
                CameraPos[1] -= ScrollSpeed*math.sin(math.radians(CameraRotate[1]))
                CameraPos[2] += ScrollSpeed*math.cos(math.radians(CameraRotate[0]))*math.cos(math.radians(CameraRotate[1]))
                CameraPos[0] -= ScrollSpeed*math.sin(math.radians(CameraRotate[0]))*math.cos(math.radians(CameraRotate[1]))
    if mpress[0]:
        Angle = math.radians(-CameraRotate[0])
        Speed = 0.1*(CameraPos[1]/50.0)
        CameraPos[0] -= (Speed*math.cos(Angle)*mrel[0])
        CameraPos[2] -= (Speed*math.sin(Angle)*-mrel[0])
        CameraPos[0] -= (Speed*math.sin(Angle)*mrel[1])
        CameraPos[2] -= (Speed*math.cos(Angle)*mrel[1])
    if mpress[2]:
        CameraRotate[0] -= 0.1*mrel[0]
        CameraRotate[1] += 0.1*mrel[1]
    if keystate[K_v]:
        CameraPos = [10,50,50]
        CameraRotate = [0,-45]
    if keystate[K_LEFT]:  Rotations[0] += 1
    if keystate[K_RIGHT]:  Rotations[0] -= 1
    if keystate[K_UP]:  Rotations[1] -= 1
    if keystate[K_DOWN]:  Rotations[1] += 1
    if keystate[K_a]:  Rotations[2] += 1
    if keystate[K_s]:  Rotations[2] -= 1
def Draw():
    #Clear
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    #Camera Position/Orient
    glRotatef(-CameraRotate[1],1,0,0)
    glRotatef( CameraRotate[0],0,1,0)
    glTranslatef(-CameraPos[0],-CameraPos[1],-CameraPos[2])
    #World
    glCallList(dlWorld)
    #Rotated Axes
    glPushMatrix()
    glRotatef(Rotations[0],0,1,0)
    glRotatef(Rotations[1],1,0,0)
    glRotatef(Rotations[2],0,1,0)
    glCallList(dlRotatedAxes)
    glPopMatrix()
    #Points
    for P in Points:
        glPushMatrix()
        Translator = GetPoint(P)
##        Translator = P
        glTranslatef(Translator[0],Translator[1],Translator[2])
        glCallList(dlSphere)
        glPopMatrix()
    #Flip
    pygame.display.flip()
def main():
    while True:
        GetInput()
        Draw()
if __name__ == '__main__': main()

















