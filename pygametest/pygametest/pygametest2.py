#!/usr/bin/env python

import random, os.path

#import basic pygame modules
import pygame
from pygame.locals import *

from SpriteUtils import *
from enum import Enum

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")


#game constants
SCREENRECT     = Rect(0, 0, 640, 480)


main_dir = os.path.split(os.path.abspath(__file__))[0]

def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s'%(file, pygame.get_error()))
    return surface.convert()

def load_images(*files):
    imgs = []
    for file in files:
        imgs.append(load_image(file))
    return imgs



# each type of game object gets an init and an
# update function. the update function is called
# once per frame, and it is when each object should
# change it's current position and state. the Player
# object actually gets a "move" function instead of
# update, since it is passed extra information about
# the keyboard


class Player(pygame.sprite.Sprite):
    
    class PlayerState(Enum):
        MOVING, NOTMOVING = range(2)

    def __init__(self, anims=[]):
        pygame.sprite.Sprite.__init__(self, self.containers)        
        self.speed = 10
        self.images = []
        self.currtime = 0
        #self.ss = spritesheet(self.file_sprite_sheet)
        self.sprite_strips = anims
        self.n = 0
        self.sprite_strips[self.n].iter()
        self.image = self.sprite_strips[self.n].next()
        self.player_state = Player.PlayerState.NOTMOVING
        #self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.reloading = 0
        self.origtop = self.rect.top
        self.facing = -1

    def move(self, direction):
        if direction: 
            self.facing = direction
        if direction == 0: 
            self.player_state = Player.PlayerState.NOTMOVING
        else:
            self.player_state = Player.PlayerState.MOVING
        self.rect.move_ip(direction*self.speed, 0)
        self.rect = self.rect.clamp(SCREENRECT)

    def update(self, *args):
        print ('elapsed time: {} ms'.format(pygame.time.get_ticks() - self.currtime))
        self.currtime = pygame.time.get_ticks()
        if (self.player_state == Player.PlayerState.MOVING):
            if (self.facing > 0):
                self.image = self.sprite_strips[self.n].next()
            elif (self.facing < 0):
                self.image = pygame.transform.flip(self.sprite_strips[self.n].next(), 1, 0)

        return super().update(*args)


def main(winstyle = 0):
    # Initialize pygame
    pygame.init()

    # Set the display mode
    winstyle = 0  # |FULLSCREEN
    bestdepth = pygame.display.mode_ok(SCREENRECT.size, winstyle, 32)
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, bestdepth)

    #decorate the game window
    #icon = pygame.transform.scale(Alien.images[0], (32, 32))
    #pygame.display.set_icon(icon)
    pygame.display.set_caption('Pygame Aliens')
    pygame.mouse.set_visible(1)

    #create the background, tile the bgd image
    bgdtile = load_image('background.gif')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 0))
    screen.blit(background, (0,0))
    pygame.display.flip()

    # Initialize Game Groups
    #aliens = pygame.sprite.Group()
    #shots = pygame.sprite.Group()
    #bombs = pygame.sprite.Group()
    all = pygame.sprite.RenderUpdates()
    #lastalien = pygame.sprite.GroupSingle()

    #assign default groups to each sprite class
    Player.containers = all

    clock = pygame.time.Clock()

    anims = ProcessSpriteSheetAnimsFromXML('randy.xml')
    player = Player(anims)

    _break = False

    while player.alive():

        #get input
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                _break = True
        keystate = pygame.key.get_pressed()

        if (_break):
            break

        # clear/erase the last drawn sprites
        all.clear(screen, background)

        #update all the sprites
        all.update()

        #handle player input
        print (keystate[K_RIGHT], keystate[K_LEFT])

        direction = keystate[K_RIGHT] - keystate[K_LEFT]
        player.move(direction)
        firing = keystate[K_SPACE]
        player.n = keystate[K_SPACE]

        #draw the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)

        #cap the framerate
        clock.tick(30)

    #end game
    pygame.quit()



#call the "main" function if running this script
if __name__ == '__main__': main()


