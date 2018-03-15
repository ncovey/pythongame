#!/usr/bin/env python

import random, os.path
import math

#import basic pygame modules
import pygame
from pygame.locals import *

from SpriteUtils import *
from enum import Enum

#see if we can load more than standard BMP
if not pygame.image.get_extended():
    raise SystemExit("Sorry, extended image module required")

import cstmmath

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


class RigidBody2D():
    def __init__(self, **kwargs):
        return super().__init__(**kwargs)




# each type of game object gets an init and an
# update function. the update function is called
# once per frame, and it is when each object should
# change it's current position and state. the Player
# object actually gets a "move" function instead of
# update, since it is passed extra information about
# the keyboard


class Player(pygame.sprite.Sprite):
    
    class PlayerMoveState(Enum):
        MOVING, NOTMOVING, JUMPING, FALLING, LANDING = range(5)

    class PlayerAnimState(Enum):
        IDLE_0, IDLE_1, RUNNING, WALKING, JUMPING, FALLING, LANDING = range(7)

    def __init__(self, anims=[]):
        pygame.sprite.Sprite.__init__(self, self.containers)        
        self.speed = 500.0
        self.jump_pow = 100.0 # ???
        self.images = []
        self.currtime = 0
        #self.ss = spritesheet(self.file_sprite_sheet)
        self.sprite_strips = anims
        self.n = 0
        self.sprite_strips[self.n].iter()
        self.image = self.sprite_strips[self.n].next()
        self.player_state = Player.PlayerMoveState.NOTMOVING
        self.player_anim_state = Player.PlayerAnimState.IDLE_0
        #self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=SCREENRECT.midbottom)
        self.facing = -1
        #self.direction = cstmmath.Vector2D(0.0, 0.0)
        self.velocity = cstmmath.Vector2D(0.0, 0.0)
        self.mass = 1.0 # ???
        self.MAX_VELOCITY = 250.0 # ???
        self.K_FRICTION = 100.0
        self.__last_acceleration = 0.0
        
    def get_strip_from_anim(self, anim_enum):
        for strip in self.sprite_strips:
            if (anim_enum == Player.PlayerAnimState.IDLE_0 and strip.name == "idle_stance_right_0"):
                return strip
            elif (anim_enum == Player.PlayerAnimState.IDLE_1 and strip.name == "idle_stance_left_0"):
                return strip
            elif (anim_enum == Player.PlayerAnimState.RUNNING and strip.name == "running"):
                return strip
            elif (anim_enum == Player.PlayerAnimState.WALKING and strip.name == "walking"):
                return strip
            elif (anim_enum == Player.PlayerAnimState.JUMPING and strip.name == "jump_straight"):
                return strip
            elif (anim_enum == Player.PlayerAnimState.FALLING and strip.name == "jump_falling"):
                return strip
            elif (anim_enum == Player.PlayerAnimState.LANDING and strip.name == "jump_landing"):
                return strip


    def move(self, direction:cstmmath.Vector2D, _dt:int, doAccelerate=True):
        #print (self.velocity.x, self.velocity.y)

        dt = (float(_dt)/1000.0)        
        
        if (doAccelerate == False):
            self.velocity = self.speed * direction
            self.rect.move_ip(self.velocity.x * dt, self.velocity.y * dt)
            self.rect = self.rect.clamp(SCREENRECT)
            return

        acceleration = direction * (self.speed / self.mass)

        print (acceleration.x, acceleration.y)
        #x0 = cstmmath.Vector2D(self.rect.x, self.rect.y)

        self.velocity += acceleration * dt
        dx = self.velocity * dt

        if (math.fabs(self.velocity.x * (direction.x)) > math.fabs(self.MAX_VELOCITY * (direction.x))):
            self.velocity.x = self.MAX_VELOCITY * (direction.x)

        print (dx.x, dx.y)
        mdx = round(dx.x)
        mdy = round(dx.y)
        self.rect.move_ip(mdx, mdy)
        self.rect = self.rect.clamp(SCREENRECT)

        

    def update(self, *args):
        dt = pygame.time.get_ticks() - self.currtime
        #print ('elapsed time: {} ms'.format(dt))
        self.currtime = pygame.time.get_ticks()
                
        #handle player input
        keystate = pygame.key.get_pressed()

        direction = cstmmath.Vector2D(0.0, 0.0)
        direction.x = keystate[K_RIGHT] - keystate[K_LEFT]
        if (math.fabs(direction.x) != 0):
            self.facing = direction.x

        if (keystate[K_SPACE] == 1):
            direction.y = (-1.0)

        doAccelerate = True

        if (direction.x != 0):
            self.player_state = Player.PlayerMoveState.MOVING
            self.n = keystate[K_LSHIFT]
            if (self.n == 1):
                self.player_anim_state = Player.PlayerAnimState.RUNNING
                self.speed = 500.0
            if (self.n == 0):
                self.player_anim_state = Player.PlayerAnimState.WALKING
                doAccelerate = False
                self.speed = 125.0
        else:
            self.player_anim_state = Player.PlayerAnimState.IDLE_0
            self.player_state = Player.PlayerMoveState.NOTMOVING
            self.velocity *= 0.0


            
        self.move(direction, dt, doAccelerate)

        #elif (keystate[K_SPACE] == 1):
        #    self.player_state = Player.PlayerMoveState.JUMPING
        #    self.player_anim_state = Player.PlayerAnimState.JUMPING
            
        #elif (keystate[K_LCTRL] == 1):
        #    self.player_state = Player.PlayerMoveState.FALLING
        #    self.player_anim_state = Player.PlayerAnimState.FALLING
            
        #elif (keystate[K_LALT] == 1):
        #    self.player_state = Player.PlayerMoveState.LANDING
        #    self.player_anim_state = Player.PlayerAnimState.LANDING       
        #else:
            #if (self.player_anim_state != Player.PlayerAnimState.IDLE_0 and 
            #    self.player_anim_state != Player.PlayerAnimState.IDLE_1):
            #    if (random.randint(0,1) == 0):
            #        self.player_anim_state = Player.PlayerAnimState.IDLE_0 
            #    else:
            #        self.player_anim_state = Player.PlayerAnimState.IDLE_1
            
        strip = self.get_strip_from_anim(self.player_anim_state)

        if (self.facing > 0):
            self.image = strip.animate(dt)
        elif (self.facing < 0):
            self.image = pygame.transform.flip(strip.animate(dt), 1, 0)

        x = self.rect.x
        y = self.rect.y
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

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
    pygame.display.set_caption('Randy')
    pygame.mouse.set_visible(1)

    #create the background, tile the bgd image
    bgdtile = load_image('..\\assets\\BKG03.png')
    background = pygame.Surface(SCREENRECT.size)
    for x in range(0, SCREENRECT.width, bgdtile.get_width()):
        background.blit(bgdtile, (x, 480-1024))
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

    while (True):

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
        
        #draw the scene
        dirty = all.draw(screen)
        pygame.display.update(dirty)
        
        
        pygame.draw.rect(screen, (255,0,0), player.rect, 2)
        screen.blit(player.image, player.rect)
        
        pygame.display.flip()

        #cap the framerate
        clock.tick(60)

    #end game
    pygame.quit()



#call the "main" function if running this script
if __name__ == '__main__': main()


