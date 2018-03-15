# This class handles sprite sheets https://www.pygame.org/wiki/Spritesheet
# This was taken from www.scriptefun.com/transcript-2-using
# sprite-sheets-and-drawing-the-background
# I've added some code to fail if the file wasn't found..
# Note: When calling images_at the rect is the format:
# (x, y, x + offset, y + offset)


#Here is a quick example on how you would use this
#    import spritesheet

#    ss = spritesheet.spriteshee('somespritesheet.png')
#    # Sprite is 16x16 pixels at location 0,0 in the file...
#    image = ss.image_at((0, 0, 16, 16))
#    images = []
#    # Load two images into an array, their transparent bit is (255, 255, 255)
#    images = ss.images_at((0, 0, 16, 16),(17, 0, 16,16), colorkey=(255, 255, 255))

import pygame
import xml.etree.ElementTree as ET
import warnings


class spritesheet(object):
    def __init__(self, filename):
        try:
            self.sheet = pygame.image.load(filename).convert()
        except ((pygame.error, message)):
            print ('Unable to load spritesheet image:', filename)
            raise (SystemExit, message)
    # Load a specific image from a specific rectangle
    def image_at(self, rectangle, colorkey = None):
        "Loads image from x,y,x+offset,y+offset"
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image
    # Load a whole bunch of images and return them as a list
    def images_at(self, rects, colorkey = None):
        "Loads multiple images, supply a list of coordinates" 
        return [self.image_at(rect, colorkey) for rect in rects]
    # Load a whole strip of images
    def load_strip(self, rect, image_count, colorkey = None):
        "Loads a strip of images and returns them as a list"
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

#
#
#
class SpriteStripAnim(object):
    """sprite strip animator
    
    This class provides an iterator (iter() and next() methods), and a
    __add__() method for joining strips which comes in handy when a
    strip wraps to the next row.
    """
    def __init__(self, filename, name, rect=None, count=0, colorkey=None, loop=False, fps=-1.0, framelist=[]):
        """construct a SpriteStripAnim
        
        filename, rect, count, and colorkey are the same arguments used
        by spritesheet.load_strip.
        
        loop is a boolean that, when True, causes the next() method to
        loop. If False, the terminal case raises StopIteration.
        
        frames is the number of ticks to return the same image before
        the iterator advances to the next image.
        """
        self.filename = filename
        self.name = name
        ss = spritesheet(filename)
        self.images = []
        if (rect != None):
            self.images = ss.load_strip(rect, count, colorkey)
        elif (len(framelist) > 0):
            for frm in framelist:
                self.images.append(ss.image_at(frm, colorkey))
        self.__image = self.images[0]
        self.current_frame = 0
        self.loop = loop
        self.__time_elapsed_ms = 0
        self.fps = fps
    def iter(self):
        self.current_frame = 0
        self.__time_elapsed_ms = 0
        return self
    def next(self):
        if self.current_frame >= len(self.images):
            if not self.loop:
                #raise StopIteration
                return self.images[self.current_frame-1]
            else:
                self.current_frame = 0
        self.__image = self.images[self.current_frame]
        self.current_frame += 1
        return self.__image
    def animate(self, dt):
        if (self.fps == -1):
            return self.next()
        self.__time_elapsed_ms += dt
        frame_dt = ((1.0/self.fps)*1000.0)
        if (self.__time_elapsed_ms >= frame_dt):
            self.__time_elapsed_ms = 0
            return self.next()
        else:
            return self.__image
    def __add__(self, ss):
        self.images.extend(ss.images)
        return self


def ProcessSpriteSheetAnimsFromXML(filename):
    animations = []
    tree = ET.parse(filename)
    root = tree.getroot()    
    img_sprite_sheet = root.get('file')
    ce = root.find('colorkey')
    colorkey = pygame.Color(int(ce.get('r')), int(ce.get('g')), int(ce.get('b')))
    for anim in root.iter('animation'):
        frames = []
        for frm in anim.iter('frame'):
            #print (frm.tag, frm.attrib)
            c = frm.find('coord')
            x=int(c.get('x'))
            y=int(c.get('y'))
            d = frm.find('dimensions')
            w=int(d.get('w'))
            h=int(d.get('h'))
            frames.append(pygame.Rect((x,y,w,h)))
            #print (coord, dim)
        name = anim.get('name')
        do_loop = (anim.get('loop').lower() == 'true')
        numframes = int(anim.get('numframes'))
        if (numframes > len(frames)):
            warnings.warn("frame number specified for the animation '{}' is greater than number of XML elements in file: '{}' (Expected {}, found {}).".format(name, filename, numframes, len(frames)))
        if (numframes < len(frames)):
            warnings.warn("frame number specified for the animation '{}' is less than the actual number of XML elements in file: '{}'. The last {} frame elements will be ignored.".format(name, filename, (len(frames)-numframes)))
        fps = int(anim.get('fps'))
        animation = SpriteStripAnim(img_sprite_sheet, name, None, numframes, colorkey, do_loop, fps, frames)
        animations.append(animation)
    return animations
