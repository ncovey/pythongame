#!/usr/bin/env python

import random, os.path

#import basic pygame modules
import pygame
from pygame.locals import *

from euclid import *

import pyglet
from pyglet.gl import *
from pyglet.window import key


'''Displays a rotating torus using the pyglet.graphics API.

This example is very similar to examples/opengl.py, but uses the
pyglet.graphics API to construct the indexed vertex arrays instead of
using OpenGL calls explicitly.  This has the advantage that VBOs will
be used on supporting hardware automatically.

The vertex list is added to a batch, allowing it to be easily rendered
alongside other vertex lists with minimal overhead.

It also show a FPS display, HTML-Text and keyboard control.
This is the basic code for the GLSL-Examples on http://www.pythonstuff.org
'''
html = '''
<font size=+3 color=#FF3030>
<b>Pyglet Basic OpenGL Demo</b>
</font><br/>
<font size=+2 color=#00FF60>
R = Reset<br/>
Q, Esc = Quit<br/>
F = Toggle Figure<br/>
T = Toggle Wireframe<br/>
W, S, A, D = Up, Down, Left, Right<br/>
Space = Move/Stop<br/>
Arrows = Move Light 0<br/>
H = This Help<br/>
</font>
'''
    
#rot = Vector3(0, 0, 90)
#autorotate = True
#rotstep = 10
#lightstep = 10 * pi / 180
#togglefigure = False
#togglewire = False
#showdialog = True

try:
    # Try and create a window with multisampling (antialiasing)
    config = Config(sample_buffers=1, samples=4,
                    depth_size=16, double_buffer=True,)
    window = pyglet.window.Window(resizable=True, config=config, vsync=False) # "vsync=False" to check the framerate
except pyglet.window.NoSuchConfigException:
    # Fall back to no multisampling for old hardware
    window = pyglet.window.Window(resizable=True)

label = pyglet.text.HTMLLabel(html, # location=location,
                              width=window.width//2,
                              multiline=True, anchor_x='center', anchor_y='center')

fps_display = pyglet.clock.ClockDisplay() # see programming guide pg 48

# Define a simple function to create ctypes arrays of floats:
def vec(*args):
    return (GLfloat * len(args))(*args)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glLoadIdentity()
    glTranslatef(0.0, 0.0, -3.5);
    #glRotatef(rot.x, 0, 0, 1)
    #glRotatef(rot.y, 0, 1, 0)
    #glRotatef(rot.z, 1, 0, 0)

    #if togglewire:
    #    glPolygonMode(GL_FRONT, GL_LINE)
    #else:
    #    glPolygonMode(GL_FRONT, GL_FILL)

    #if togglefigure:
    #    batch1.draw()
    #else:
    #    batch2.draw()

    #if togglewire:
    #    glPolygonMode(GL_FRONT, GL_FILL)

    glActiveTexture(GL_TEXTURE0)
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    #if showdialog:
    glLoadIdentity()
    glTranslatef(0, -200, -450)
    label.draw()

    glLoadIdentity()
    glTranslatef(250, -290, -500)
    fps_display.draw()

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glDisable(GL_TEXTURE_2D)

@window.event
def on_resize(width, height):
    if height==0: height=1
    # Keep text vertically centered in the window
    label.y = window.height // 2
    # Override the default on_resize handler to create a 3D projection
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60., width / float(height), .1, 1000.)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED

def update(dt):
    #get input
    for event in pygame.event.get():
        if (event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE):
            return
    keystate = pygame.key.get_pressed()
    #cap the framerate
    clock.tick(40)

pyglet.clock.schedule(update)

def dismiss_dialog(dt):
    global showdialog
    showdialog = False
pyglet.clock.schedule_once(dismiss_dialog, 10.0)


def setup():
    # One-time GL setup
    global light0pos
    global light1pos
    global togglewire

    light0pos = [20.0,   20.0, 20.0, 1.0] # positional light !
    light1pos = [-20.0, -20.0, 20.0, 0.0] # infinitely away light !

    glClearColor(1, 1, 1, 1)
    glColor4f(1.0, 0.0, 0.0, 0.5 )
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_CULL_FACE)

    # Uncomment this line for a wireframe view
    #glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Simple light setup.  On Windows GL_LIGHT0 is enabled by default,
    # but this is not the case on Linux or Mac, so remember to always
    # include it.
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    glLightfv(GL_LIGHT0, GL_POSITION, vec(*light0pos))
    glLightfv(GL_LIGHT0, GL_AMBIENT, vec(0.3, 0.3, 0.3, 1.0))
    glLightfv(GL_LIGHT0, GL_DIFFUSE, vec(0.9, 0.9, 0.9, 1.0))
    glLightfv(GL_LIGHT0, GL_SPECULAR, vec(1.0, 1.0, 1.0, 1.0))

    glLightfv(GL_LIGHT1, GL_POSITION, vec(*light1pos))
    glLightfv(GL_LIGHT1, GL_DIFFUSE, vec(.6, .6, .6, 1.0))
    glLightfv(GL_LIGHT1, GL_SPECULAR, vec(1.0, 1.0, 1.0, 1.0))

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, vec(0.8, 0.5, 0.5, 1.0))
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, vec(1, 1, 1, 1))
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 50)

################
## Entry point #
################
def main(winstyle = 0):

    setup()

    #batch1  = pyglet.graphics.Batch()
    #torus = Torus(1, 0.3, 80, 25, batch=batch1)
    #batch2  = pyglet.graphics.Batch()
    #sphere = Sphere(1.2, 4, batch=batch2)
    
    pyglet.app.run()


    #SCREENRECT     = Rect(0, 0, 640, 480)
    # Initialize pygame
    pygame.init()

    # Set the display mode
    #winstyle = 0  # |FULLSCREEN
    #bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    #screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)
    
    #background = pygame.Surface(SCREENRECT.size)
    #screen.blit(background, (0,0))
    #pygame.display.flip()


    mainloop()
    

    pygame.quit()



#call the "main" function if running this script
if (__name__ == '__main__'):
    main()